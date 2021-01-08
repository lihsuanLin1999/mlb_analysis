import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

year_list = [2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]
scenario_list = ["h", "a", "d", "n", "vl", "vr", "sah", "sbh", "sti", "r0", "r1", "r12", "r123", "ron",
                 "ron2", "risp", "risp2", "o0", "o1", "o2", "ac", "bc", "ec", "2s", "fc"]
page_list = range(1, 50)

def mlb_scrape_player_stat(url, poistion_exist, col_name, col_num_specific, file_path):
    for year in year_list:
        for scenario in scenario_list:
            print(scenario)

            appended_data = []

            for page_num in page_list:
                print("process " + str(year) + " ," + scenario + " ,page: " + str(page_num))
                full_url = url + str(year) + "?split=" + scenario + "&page=" + str(page_num) + "&playerPool=ALL"
                page = requests.get(full_url)
                time.sleep(1)

                soup = BeautifulSoup(page.content, 'lxml')

                table = soup.find('table', attrs={'class':'bui-table is-desktop-sKqjv9Sb'})
                table_rows = table.find_all('tr')
                l = []

                for tr in table_rows:
                    td = tr.find_all('td')
                    row = [tr.text for tr in td]
                    l.append(row)

                df = pd.DataFrame(l)
                df = df.iloc[1:]

                if df.empty:
                    print("page not exist. Process next")
                    break

                #get name and url
                productDivs = soup.findAll('div', attrs={'class' : 'top-wrapper-1NLTqKbE'})

                url_list = []
                name_list = []
                position_list = []
                url_first_part = "https://www.mlb.com"

                try:
                    for div in productDivs:
                        url_second_part = div.find('a')['href']
                        url_link = url_first_part + url_second_part
                        url_list.append(url_link)
                        name = div.find('a')['aria-label']
                        name_list.append(name)

                        if poistion_exist:
                            position = div.find('div', attrs={'class': 'position-28TbwVOg'}).text
                            position_list.append(position)

                except KeyError:
                    print("encounter error")

                df.insert(0, "player", name_list)
                if poistion_exist:
                    df.insert(1, "position", position_list)

                df.insert(col_num_specific, "url", url_list)
                df.columns = col_name
                appended_data.append(df)
                #end of page for loop

            df_output = pd.concat(appended_data)
            file_name = file_path + str(year) + "/" + str(year) + "-" + scenario + ".csv"
            df_output.to_csv(file_name, index=False)
            print(str(year) + "-" + scenario + " completed!")



# url = "https://www.mlb.com/stats/"
# position_exist = true
# col_name = ["player", "position", "team", "G", "AB", "R", "H", "2B", "3B", "HR","RBI", "BB", "SO", "SB", "CS", "AVG", "OBP", "SLG", "OPS", "url"]
# col_num_specific = 19
# file_path = "/Users/leechilin/Desktop/python scrape/data_MLB_PLAYER_BATTER/"
#
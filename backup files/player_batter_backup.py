import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

year_list = [2013, 2012, 2011, 2010]
scenario_list = ["h","a", "d", "n", "vl", "vr", "sah", "sbh"]
# "h","a", "d", "n", "vl", "vr",
  #easy way since pages won't be longer than 50 pages
page_list = range(1, 50)

for year in year_list:
    for scenario in scenario_list:
        print(scenario)

        appended_data = []

        for page_num in page_list:
            print("process " + str(year) + " ," + scenario + " ,page: " + str(page_num))
            url = "https://www.mlb.com/stats/" + str(year) + "?split=" + scenario + "&page=" + str(page_num) + "&playerPool=ALL"
            page = requests.get(url)
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

                    position = div.find('div', attrs={'class': 'position-28TbwVOg'}).text
                    position_list.append(position)

            except KeyError:
                print("encounter error")

            df.insert(0, "player", name_list)
            df.insert(1, "position", position_list)
            df.insert(19, "url", url_list)
            df.columns = ["player", "position", "team", "G", "AB", "R", "H", "2B", "3B", "HR",
                          "RBI", "BB", "SO", "SB", "CS", "AVG", "OBP", "SLG", "OPS", "url"]
            appended_data.append(df)
            #end of page for loop

        df_output = pd.concat(appended_data)
        file_name = "/Users/leechilin/Desktop/python scrape/data_MLB_PLAYER_BATTER/" + str(year) + "/" + str(year) + "-" + scenario + ".csv"
        df_output.to_csv(file_name, index=False)
        print(str(year) + "-" + scenario + " completed!")
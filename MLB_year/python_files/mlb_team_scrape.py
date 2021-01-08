import requests
import pandas as pd
from bs4 import BeautifulSoup



def mlb_scrape_team_stats(year_list, scenario_list, url, col_specific, col_num_specific, col_name, file_path):
    for year in year_list:
        for scenario in scenario_list:

            full_url = url + str(year) + "?split=" + scenario
            page = requests.get(full_url)
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

            #get name and url
            productDivs = soup.findAll('div', attrs={'class' : 'top-wrapper-1NLTqKbE'})

            url_list = []
            name_list = []
            url_first_part = "https://www.mlb.com"

            try:
                for div in productDivs:
                    url_second_part = div.find('a')['href']
                    url_link = url_first_part + url_second_part
                    url_list.append(url_link)
                    name = div.find('a')['aria-label']
                    name_list.append(name)

            except KeyError:
                print("encounter error")

            df.insert(0, col_specific[0], name_list)
            df.insert(col_num_specific, col_specific[1], url_list)
            df.columns = col_name
            file_name = file_path + str(year) + "-" + scenario + ".csv"
            df.to_csv(file_name, index=False)
            print(str(year) + "-" + scenario + " completed!")





















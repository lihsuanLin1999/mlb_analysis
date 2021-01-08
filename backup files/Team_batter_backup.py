import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

year_list = [2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]
scenario_list = ["h","a", "d", "n", "vl", "vr", "sah", "sbh", "sti", "r0", "r1", "r12", "r123", "ron",
                 "ron2", "risp", "risp2", "o0", "o1", "o2", "ac", "bc", "ec", "2s", "fc"]

for year in year_list:
    for scenario in scenario_list:

        url = "https://www.mlb.com/stats/team/" + str(year) + "?split=" + scenario
        page = requests.get(url)
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

        df.insert(0, "team", name_list)
        df.insert(18, "url", url_list)
        df.columns = ["team", "league", "G", "AB", "R", "H", "2B", "3B", "HR", "RBI", "BB", "SO", "SB", "CS",
                      "AVG", "OBP", "SLG", "OPS", "url"]
        file_name = "/Users/leechilin/Desktop/python scrape/data_MLB_TEAM_BATTER/" + str(year) + "-" + scenario + ".csv"
        df.to_csv(file_name, index=False)
        print(str(year) + "-" + scenario + " completed!")



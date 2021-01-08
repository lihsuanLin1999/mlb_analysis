import pandas as pd
import requests
import re
import time
from bs4 import BeautifulSoup


# df1 = pd.read_csv("/Users/leechilin/Desktop/python scrape/basic_info_1.csv")
# df2 = pd.read_csv("/Users/leechilin/Desktop/python scrape/basic_info_2.csv")
# df_new = pd.concat([df1, df2]).drop_duplicates('id').reset_index(drop=True)


# df_new = pd.read_csv("/Users/leechilin/Desktop/python scrape/basic_info_full.csv")
# df_pitcher = df_new.loc[df_new['position'] == 'P']
# df_batter = df_new.loc[df_new['position'] != 'P']
# print(len(df_batter))

# df_pitcher.to_csv("/Users/leechilin/Desktop/python scrape/basic_info_pitcher.csv")
# df_batter.to_csv("/Users/leechilin/Desktop/python scrape/basic_info_batter.csv")

# df = pd.read_csv("/Users/leechilin/Desktop/python scrape/batter_id.csv")
# player_id_list = df["batter_id"].to_list()
#
# url_part = "https://baseballsavant.mlb.com/savant-player/"
# url_lst = [url_part + str(player_id) for player_id in player_id_list]
# df_new = pd.DataFrame(url_lst)
# df_new.to_csv("/Users/leechilin/Desktop/python scrape/url.csv")

# url = "https://baseballsavant.mlb.com/savant-player/tony-barnette-501817?stats=career-r-pitching-mlb"
# page = requests.get(url)
# soup = BeautifulSoup(page.content, "html.parser")
# career_stats_html = soup.find("div", {"id": "pitchingStandard"})
# career_stats_body_html = career_stats_html.findAll("tr")
#
# num = 0
# for item in career_stats_body_html:
#     if num == 0:
#         pass
#     elif num == len(career_stats_body_html) -1:
#         pass
#     else:
#         word_list = item.text.strip()
#         word_clean = word_list.split(" ")
#         print(word_clean)
#
#     num = num + 1

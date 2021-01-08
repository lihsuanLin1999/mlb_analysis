#goal
#get all the batter id and pitcher id

import glob
import pandas as pd
import re

def get_id(path_name):
    year_list = range(2010, 2021)
    id_set = set()
    for year in year_list:
        path = path_name + str(year) + "/*.csv"
        for fname in glob.glob(path):
            print(fname)
            df = pd.read_csv(fname)
            url_local = df["url"]
            for url in url_local:
                match = re.search(pattern="[0-9]+", string=url)
                match_num = match.group(0)
                id_set.add(match_num)
    id_list = list(id_set)
    return id_list



if __name__  == "__main__":
    path_batter = "/Users/leechilin/Desktop/python scrape/data_MLB_PLAYER_PTICH/"
    path_pitcher = "/Users/leechilin/Desktop/python scrape/data_MLB_PLAYER_BATTER/"

    id_pitcher_list = get_id(path_pitcher)
    id_batter_list = get_id(path_batter)


    df_pitcher_id = pd.DataFrame(id_pitcher_list, columns = ["pitcher_id"])
    df_batter_id = pd.DataFrame(id_batter_list, columns= ["batter_id"])

    df_pitcher_id.to_csv("/Users/leechilin/Desktop/python scrape/pitcher_id.csv")
    df_batter_id.to_csv("/Users/leechilin/Desktop/python scrape/batter_id.csv")





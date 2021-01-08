import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import concurrent.futures
import csv
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count


basic_info_table = []

def scrape_basic_info(url_lst):
    """column name: ["id", "name", "picture", "position", "B/P", "weight", "height", "age"]"""

    url_string = re.search(pattern="[0-9]+", string=url_lst)
    url_id = url_string.group()
    print("process " + str(url_id))

    page = requests.get(url_lst)

    soup = BeautifulSoup(page.content, "html.parser")

    #name
    player_name = soup.find("div", {"style":"display: inline-block"}).text

    #picture
    link_pic = soup.find("img",{"class":"head-shot"})["src"]

    #basic info
    basic_info_list = []
    basic_info = soup.find("div",{"style":"font-size: .8rem;"})
    word = basic_info.text.strip()
    temp = word.split("|")

    num = 0
    for a in temp:
        word_temp = a.strip()
        if num == 0:
            basic_info_list.append(word_temp)
        elif num == 1:
            posit = re.search(pattern="(?<=:\\s).*", string=word_temp)
            basic_info_list.append(posit.group())
        elif num == 2:

            weight_raw = re.search(pattern="(?<=\"\\s).*", string=word_temp)
            weight_text = weight_raw.group()
            weight = re.search(pattern="[0-9]+", string=weight_text)
            basic_info_list.append(weight.group())

            height = re.search(pattern="^([^\"])+", string=word_temp)
            basic_info_list.append(height.group())

        elif num == 3:
            age = re.search(pattern="[0-9]+",string=word_temp)
            basic_info_list.append(age.group(0))

        num = num + 1
    basic_info_list.insert(0, player_name)
    basic_info_list.insert(1, link_pic)
    basic_info_list.insert(0, url_id)

    # print("scrape_basic_info")
    # print(basic_info_list)
    basic_info_table.append(basic_info_list)

    return basic_info_table


if __name__ == "__main__":
    df = pd.read_csv("/Users/leechilin/Desktop/python scrape/batter_id.csv")
    player_id_list = df["batter_id"].to_list()

    url_part = "https://baseballsavant.mlb.com/savant-player/"
    url_lst = [url_part + str(player_id) for player_id in player_id_list]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(scrape_basic_info, url_lst)

    col_name = ["id", "name", "picture", "position", "prefer_hand", "weight", "height","age"]
    df = pd.DataFrame(basic_info_table,columns=col_name)
    df.to_csv("/Users/leechilin/Desktop/python scrape/basic_info_2.csv")
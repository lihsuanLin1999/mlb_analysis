import requests
import pandas as pd
import re
from bs4 import BeautifulSoup


# def process_basic_info(url_path, player_id_list):
#     basic_info_table = []
#     for player_id in player_id_list:
#         print("process id: " + str(player_id))
#         url = url_path + player_id
#         soup = parse_html(url)
#         scrape_basic_info(soup, basic_info_table, player_id)
#     return (basic_info_table)


# def check_pitcher(soup):
#     basic_info = soup.find("div", {"style": "font-size: .8rem;"})
#     word = basic_info.text.strip()
#     word_list = word.split("|")
#     check_string = word_list[0].strip()
#
#     if check_string == 'P':
#         return True
#
#     return False


def scrpae(url):
    soup = parse_html(url)

    url_string = re.search(pattern="[0-9]+", string=url)
    url_id = url_string.group()

    scrape_stats_table(soup, url_id)
    scrape_stats_detail_table(soup, url_id)
    scrape_pitch_type(soup, url_id)
    scrape_pitch_track(soup, url_id)
    scrape_ball_movement(soup, url_id)
    scrape_run_values(soup, url_id)
    scrape_plate_discipline(soup, url_id)
    scrape_percent_rank(soup, url_id)



def parse_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def scrape_basic_info(soup):
    """column name: ["id", "name", "picture", "position", "B/P", "weight", "height", "age"]"""

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

    print("scrape_basic_info")
    print(basic_info_list)

def scrape_stats_table(soup, url_id):
    """column name: ["id', season_played', 'type', 'W', 'L', 'ERA', 'G', 'GS', 'SV', 'IP', 'SO', 'WHIP']"""
    stat_table = []
    row_body = soup.find("div", {"class":"non-mobile"})
    row_body_data = row_body.findAll("td",{"class":["tr-data align-left", "tr-data"]})

    #body
    data = []
    for b in row_body_data:
        data.append(b.text)

    data_interest_0 = data[0:len(data)//2 - 1]
    data_interest_1 = data[len(data)//2:len(data)]

    data_interest_0.insert(1,"most recent")
    data_interest_1.insert(1, "career")

    data_interest_0.insert(0, url_id)
    data_interest_1.insert(0, url_id)

    stat_table_big_table.append(data_interest_0)
    stat_table_big_table.append(data_interest_1)

    print("scrape stats table")
    print(stat_table)

def scrape_stats_detail_table(soup, url_id):
    """column name: ['id', 'Season', 'Pitches', 'Batted Balls', 'Barrels', 'Barrel %',
                     'Exit Velocity', 'Launch Angle', 'Sweet Spot %', 'XBA',
                     'XSLG', 'WOBA', 'XWOBA', 'XWOBACON', 'Hard Hit %', 'K %', 'BB %',
                     'ERA', 'xERA']"""
    stat_detail_table = []
    try:
        #Statcast Statistics
        stats_html = soup.find("div",{"id":"statcast_stats_pitching"})

        # header
        # stat_detail_header = []
        # stats_header_html = stats_html.findAll("th", {"class":["th-component-header align-left header table-static-column", "th-component-header align-right header"]})
        # for item in stats_header_html:
        #     stat_detail_header.append(item.text.strip())

        # body
        stats_row_html = stats_html.findAll("tr", {"class":"default-table-row"})
        for row in stats_row_html:
            row_list = []
            for col_data in row.findAll("td", {"class": ["tr-data align-left table-static-column","tr-data align-right"]}):
                if col_data.text == "":
                    word = "NA"
                else:
                    word = col_data.text
                row_list.append(word)
            stat_detail_table.append(row_list)
        stat_detail_table.insert(0, url_id)
        print("scrape stats detail table")

    except AttributeError:
        stat_detail_table = ["NA"] * 18
        stat_detail_table.insert(0,url_id)
        print("Not found stats detail table")

    print(stat_detail_table)

def scrape_pitch_type(soup, url_id):
    #pitch type
    pitch_type_list = []
    pitch_list = []
    percent_list = []

    try:
        pitch_type_html = soup.findAll("div", {"class":"spin-pitches"})
        for type in pitch_type_html:
            w = type.text.splitlines()
            word_list = list(filter(None, w))

            pitch_type = word_list[0]
            percent_raw = re.search(pattern="(?<=\\().+?(?=\\))",string=word_list[1])
            percent = percent_raw.group()

            pitch_list.append(pitch_type)
            percent_list.append(percent)

        pitch_list.insert(0, url_id)
        percent_list.insert(0, url_id)

        if len(pitch_list) == 1:
            pitch_list.append("NA")
        if len(percent_list) == 1:
            percent_list.append("NA")

        pitch_type_list.append(pitch_list)
        pitch_type_list.append(percent_list)

        print("scrape_pitch_type, possibly not found")

    except AttributeError:
        pitch_type_list = ["NA"] * 1
        pitch_type_list.insert(0, url_id)
        print("Not found pitch type table")

    print(pitch_type_list)

def scrape_pitch_track(soup, url_id):
    """column name: ['Year', 'Pitch Type', '#', '# RHB', '# LHB', '%', 'MPH',
                     'PA', 'AB', 'H', '1B', '2B', '3B', 'HR', 'SO', 'BBE', 'BA',
                     'XBA', 'SLG', 'XSLG', 'WOBA', 'XWOBA', 'EV', 'LA', 'Spin',
                     'Whiff%', 'PutAway%']"""
    # pitch Tracking
    pitch_track_table = []
    pitch_track_table_modify = []
    try:
        pitch_track_html = soup.find("div", {"id":"pitchTable"})
        pitch_track_body_html = pitch_track_html.findAll("tr")

        for item in pitch_track_body_html:
            word_list = item.text.strip().splitlines()
            word_list_modify = [name for name in word_list if name.strip()]
            pitch_track_table.append(word_list_modify)

        pitch_track_table_modify = pitch_track_table[1:]
        pitch_track_table_modify.insert(0, url_id)
        print("scrape_pitch_track")

    except AttributeError:
        pitch_track_table_modify = ["NA"] * 27
        pitch_track_table_modify.insert(0, url_id)
        print("Not found pitch track table")

    print(pitch_track_table_modify)

def scrape_ball_movement(soup, url_id):
    """column name:['Year', 'Pitch', 'Team', 'Hand', '#', 'MPH',
                    'Inches of Drop', 'vs Avg', '% vs Avg', 'Inches of Break',
                    'vs Avg', '% Break vs Avg']"""
    #ball movement:
    pitch_movement_table = []
    pitch_movement_table_modify = []

    try:
        pitch_movement_html = soup.find("table",{"id": "pitchMovement"})
        pitch_movement_header_html = pitch_movement_html.findAll("tr")

        for item in pitch_movement_header_html:
            word_list = item.text.strip().splitlines()
            word_list_modify = [name for name in word_list if name.strip()]
            pitch_movement_table.append(word_list_modify)

        pitch_movement_table_modify = pitch_movement_table[2:]
        pitch_movement_table_modify.insert(0, url_id)
        print("scrape_ball_movement")

    except AttributeError:
        pitch_movement_table_modify = ["NA"] * 12
        pitch_movement_table_modify.insert(0, url_id)
        print("Not found ball movement table")

    print(pitch_movement_table_modify)

def scrape_run_values(soup, url_id):
    """column name: ['Year', 'Pitch Type', 'RV/100', 'Run Value',
                     'Pitches', '%', 'PA', 'BA', 'SLG', 'wOBA',
                     'Whiff%', 'K%', 'PutAway %', 'xBA', 'xSLG',
                     'xwOBA', 'Hard Hit %']"""
    # run_values_header = []
    # run_values_head_html = run_values_html.findAll("th")
    # for item in run_values_head_html:
    #     run_values_header.append(item.text)
    # run_values_header.remove("Team")

    #run values by pitch type
    run_values_table = []
    try:
        run_values_html = soup.find("table",{"id":"runValues"})

        run_values_body_html = run_values_html.findAll("tr")
        for item in run_values_body_html:
            word_list = item.text.strip().splitlines()
            word_list_modify = [name for name in word_list if name.strip()]
            run_values_table.append(word_list_modify)

        run_values_table.insert(0, url_id)
        print("scrape_run_values")

    except AttributeError:
        run_values_table = ["NA"] * 17
        run_values_table.insert(0, url_id)
        print("Not found run values table")

    print(run_values_table)

def scrape_plate_discipline(soup, url_id):
    """column name: ['Season', 'Pitches', 'Zone %', 'Zone Swing %', 'Zone Contact %',
                     'Chase %', 'Chase Contact %', 'Edge %', '1st Pitch Strike %', 'Swing %',
                     'Whiff %', 'Meatball %', 'Meatball Swing %']"""
    #plate discipline
    plate_dis_table = []
    plate_dis_table_modify = []

    try:
        plate_dis_html = soup.find("table", {"id": "playeDiscipline"})
        plate_dis_body_html = plate_dis_html.findAll("tr")
        for item in plate_dis_body_html:
            word_list = item.text.strip().splitlines()
            word_list_modify = [name for name in word_list if name.strip()]
            row = []
            for word in word_list_modify:
                row.append(word.strip())
            plate_dis_table.append(row)

        plate_dis_table_modify = plate_dis_table[1:]
        plate_dis_table_modify.insert(0, url_id)
        print("scrape_plate_discipline")

    except AttributeError:
        plate_dis_table_modify = ["NA"] * 13
        plate_dis_table_modify.insert(0, url_id)
        print("Not found plate discipline table")

    print(plate_dis_table_modify)

def scrape_percent_rank(soup, url_id):
    """column name: ['Year', 'xwOBA', 'xBA', 'xSLG', 'xISO', 'xOBP',
                     'Brl', 'Brl%', 'EV', 'HardHit%', 'K%', 'BB%',
                     'Whiff%', 'xERA', 'FB Velo', 'FB Spin', 'CB Spin']"""
    #percentile ranking
    percent_rank_table = []
    percent_rank_table_modify = []

    try:
        percent_rank_html = soup.find("table", {"id":"percentileRankings"})
        percent_rank_body_html = percent_rank_html.findAll("tr")
        for item in percent_rank_body_html:
            word_list = item.text.strip().splitlines()
            percent_rank_table.append(word_list)

        percent_rank_table_modify = percent_rank_table[1:]
        print("scrape_percent_rank")

    except AttributeError:
        percent_rank_table_modify = ["NA"] * 17
        percent_rank_table_modify.insert(0, url_id)
        print("Not found percent rank table")

    print(percent_rank_table_modify)



if __name__ == '__main__':
    url_path = "https://baseballsavant.mlb.com/savant-player/519242"
    scrpae(url_path)

    print()
    print()
    print()

    url_path = "https://baseballsavant.mlb.com/savant-player/493416"
    scrpae(url_path)





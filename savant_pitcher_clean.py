import pandas as pd
import glob
import os


column_list = [['id', 'Season', 'Pitches', 'Batted Balls', 'Barrels', 'Barrel %','Exit Velocity',
                'Launch Angle', 'Sweet Spot %', 'XBA','XSLG', 'WOBA', 'XWOBA', 'XWOBACON',
                'Hard Hit %', 'K %', 'BB %','ERA', 'xERA'],
               ['id', 'Year', 'xwOBA', 'xBA', 'xSLG', 'xISO', 'xOBP','Brl', 'Brl%', 'EV',
                'HardHit%', 'K%', 'BB%','Whiff%', 'xERA', 'FB Velo', 'FB Spin', 'CB Spin'],

               ['id','Year', 'Pitch Type', 'RV/100', 'Run Value','Pitches', '%', 'PA', 'BA', 'SLG', 'wOBA',
                'Whiff%', 'K%', 'PutAway %', 'xBA', 'xSLG','xwOBA', 'Hard Hit %'],

               ['id','Year', 'Pitch', 'Team', 'Hand', '#', 'MPH','Inches of Drop', 'vs Avg', '% vs Avg',
                'Inches of Break','vs Avg', '% Break vs Avg'],

               ['id', 'Year', 'Pitch Type', '#', '# RHB', '# LHB', '%', 'MPH','PA', 'AB',
                'H', '1B', '2B', '3B', 'HR', 'SO', 'BBE', 'BA','XBA', 'SLG', 'XSLG',
                'WOBA', 'XWOBA', 'EV', 'LA', 'Spin','Whiff%', 'PutAway%'],

               ['id','Season', 'Pitches', 'Zone %', 'Zone Swing %', 'Zone Contact %','Chase %',
                'Chase Contact %', 'Edge %', '1st Pitch Strike %', 'Swing %',
                'Whiff %', 'Meatball %', 'Meatball Swing %'],

               ['id', 'type', 'proportion'],

               ["id", "Year", "team", "league", "BF", "W","L", "ERA", "G", "GS", "SV",
                "IP", "H", "R","ER", "HR", "BB", "SO", "WHIP"],

               ['id', 'season_played', 'type', 'W', 'L', 'ERA', 'G', 'GS',
                'SV','IP', 'SO', 'WHIP']]


os.chdir("/Users/leechilin/Desktop/python scrape/new_folder")
num = 0
for file in glob.glob("*.csv"):
    print(file)
    df = pd.read_csv("/Users/leechilin/Desktop/python scrape/new_folder/" + file)

    first_column = df.columns[0]

    # Delete first
    df = df.drop([first_column], axis=1)

    #get first row
    df_first_row = list(df.columns)
    first_row_len = len(df_first_row)
    df_first_row_modify = ["NA"] * (first_row_len-1)
    df_first_row_modify.insert(0, df_first_row[0])

    #insert at top
    df.loc[-1] = df_first_row_modify
    df.index = df.index + 1
    df.sort_index(inplace=True)
    df.columns = column_list[num]
    df.fillna("NA", inplace=True)
    df.to_csv("/Users/leechilin/Desktop/python scrape/pitcher/" + file, index=False)
    num = num + 1





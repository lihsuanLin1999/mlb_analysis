from mlb_scrape import *
from selenium import webdriver



if __name__ == '__main__':
    browser = webdriver.Chrome(executable_path="/Users/leechilin/Desktop/python scrape/chromedriver")
    year_list = [2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]


    col_num = 17
    for year in year_list:

        # first part scrape
        name_list = []
        position_list = []

        # second part scrape
        team_list = []
        G_list = []
        AB_list = []
        R_list = []
        H_list = []
        sec_hit_list = []
        thd_hit_list = []
        HR_list = []
        RBI_list = []
        BB_list = []
        SO_list = []
        SB_list = []
        CS_list = []
        AVG_list = []
        OBP_list = []
        SLG_list = []
        OPS_list = []

        big_list = [team_list, G_list, AB_list, R_list, H_list, sec_hit_list, thd_hit_list, HR_list,
                    RBI_list, BB_list, SO_list, SB_list, CS_list, AVG_list, OBP_list, SLG_list, OPS_list]

        scrape_mlb(year, browser, name_list, position_list, big_list, col_num)
        print("scrape " + str(year) + " completed")

        export_csv(big_list, year)
        print("export " + str(year) + " completed")
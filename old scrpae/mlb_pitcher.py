from mlb_scrape import *
from selenium import webdriver

if __name__ == '__main__':
    browser = webdriver.Chrome(executable_path="/Users/leechilin/Desktop/python scrape/chromedriver")
    year_list = [2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]

    #different scenario
    scenario_list = ["h", "a", "d", "n", "vl", "vr", "sah", "sbh", "sti", "r0", "r1", "r12","r123", "ron",
                     "ron2", "risp", "risp2", "o0", "o1", "o2", "ac", "bc", "ec", "2s", "fc"]

    # column name
    col_name_list = ["name", "team", "W", "L", "ERA", "G", "GS", "CG", "SHO", "SV", "SVO", "IP", "H", "R",
                     "ER", "HR", "HB", "BB", "SO", "WHIP", "AVG"]


    ncol = 19
    for year in year_list:


        #do not scrape position
        position_exist = False

        #url_path
        for scenario in scenario_list:
            # first part scrape
            name_list = []
            position_list = []

            # second part scrape
            team_list = []
            W_list = []
            L_list = []
            ERA_list = []
            G_list = []
            GS_list = []
            CG_list = []
            SHO_list = []
            SV_list = []
            SVO_list = []
            IP_list = []
            H_list = []
            R_list = []
            ER_list = []
            HR_list = []
            HB_list = []
            BB_list = []
            SO_list = []
            WHIP_list = []
            AVG_list = []

            big_list = [team_list, W_list, L_list, ERA_list, G_list, GS_list, CG_list, SHO_list,
                        SV_list, SVO_list, IP_list, H_list, R_list, ER_list, HR_list, HB_list, BB_list, SO_list,
                        WHIP_list, AVG_list]

            url_path = "https://www.mlb.com/stats/pitching/" + str(year) + "?split=" + scenario + "&playerPool=ALL"
            print(url_path)
            scrape_mlb(year, browser, name_list, position_list, big_list, ncol, position_exist, url_path)
            print("scrape " + str(year) + "/" + scenario + " completed")

            filename = "/Users/leechilin/Desktop/python scrape/" + str(year) + "-" + scenario + ".csv"
            export_csv(big_list, col_name_list, filename)
            print("export " + str(year) + " completed")

    print("All done!!")







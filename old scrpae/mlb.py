from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
import pandas as pd

#This is just temp file

def scrape_player_posit(name_list, position_list):

    player_html = WebDriverWait(browser, 15).until(
        EC.presence_of_all_elements_located((By.XPATH, ".//span[@class='full-3fV3c9pF']")))

    c = ""
    num = 0
    for x in player_html:
        if num % 2 == 0:
            a = x.text
            c = c + a + " "
        else:
            a = x.text
            c = c + a
            name_list.append(c)
            c = ""
        num = num + 1

    position_html = WebDriverWait(browser, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "position-28TbwVOg")))

    for x in position_html:
        word = x.text
        position_list.append(word)

    return len(position_html)

def scrape_stats(length_player, big_list):
    a = "//*[@id='stats-app-root']/div/section/section/div[3]/div[1]/div/table/tbody/tr["
    b = "]/td["
    c = "]"

    for i in range(1, length_player+1):
        for j in range(1, 18):
            path = a + str(i) + b + str(j) + c
            place_holder = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, path)))

            word = place_holder.text

            big_list[j-1].append(word)

def auto_scrape(name_list, position_list, big_list):
    a = 3
    while True:
        try:
            #set up scraping process
            element = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@id='stats-app-root']/div/section/section/div[3]/div[2]/div/div/div[3]/button")))
            element.click()
            time.sleep(20)

            #scraping part
            length_of_player = scrape_player_posit(name_list, position_list)
            scrape_stats(length_of_player, big_list)
            print("page " + str(a) + ":")
            print("scrape " + str(length_of_player) + " rows")
            print("Total row: " + str(len(name_list)))
            #increment page num
            a = a + 1

        except TimeoutException:
            print("Time out exception! ")
            break
    print("scrape ends")

def scrape_mlb(year):
    # Establish chrome driver and go to report site URL
    print("process year " + str(year))
    url_path = "https://www.mlb.com/stats/" + str(year) + "?playerPool=ALL"
    browser.get(url_path)
    time.sleep(15)

    #first part scrape
    name_list = []
    position_list = []

    #second part scrape
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

    #accept the website cookie
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))).click()
    except TimeoutException:
        pass

    time.sleep(15)

    # #scrape the first page
    length_n_player = scrape_player_posit(name_list, position_list)
    scrape_stats(length_n_player, big_list)
    print("page 1: ")
    print("scrape " + str(length_n_player) + " rows")
    print("Total row: " + str(len(name_list)))

    # go to the second page first since html/css different
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='stats-app-root']/div/section/section/div[3]/div[2]/div/div/div[2]/button"))).click()

    time.sleep(15)
    length_of_player = scrape_player_posit(name_list, position_list)
    scrape_stats(length_of_player, big_list)
    print("page 2: ")
    print("scrape " + str(length_of_player) + " rows")
    print("Total row: " + str(len(name_list)))

    # #automate the scraping part
    auto_scrape(name_list, position_list, big_list)

    # merge column
    big_list.insert(0, position_list)
    big_list.insert(0, name_list)

    # #TODO: create dataframe
    data = pd.DataFrame(big_list).transpose()
    data.columns = ["name", "position", "team", "G", "AB", "R", "H", "2B", "3B", "HR", "RBI", "BB", "SO", "SB", "CS", "AVG", "OBP", "SLG", "OPS"]
    file_name = "/Users/leechilin/Desktop/python scrape/" + str(year) + ".player.csv"
    data.to_csv(file_name, index = False)

if __name__ == '__main__':
    browser = webdriver.Chrome(executable_path="/Users/leechilin/Desktop/python scrape/chromedriver")
    year_list = [2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]
    for year in year_list:
        scrape_mlb(year)
    print("scrape has finally ended")


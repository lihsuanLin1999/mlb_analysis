from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
import pandas as pd

#This is just temp file

def scrape_player_posit(name_list, position_list, browser, position_exist):

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

    if position_exist:
        position_html = WebDriverWait(browser, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "position-28TbwVOg")))

        for x in position_html:
            word = x.text
            position_list.append(word)

    length_page = len(player_html) * 1/2

    return int(length_page)

def scrape_stats(length_player, big_list, browser, col_num):
    a = "//*[@id='stats-app-root']/div/section/section/div[3]/div[1]/div/table/tbody/tr["
    b = "]/td["
    c = "]"

    for i in range(1, length_player + 1):
        for j in range(1, col_num + 1):
            path = a + str(i) + b + str(j) + c

            place_holder = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, path)))
            word = place_holder.text
            big_list[j-1].append(word)

def auto_scrape(name_list, position_list, big_list, browser, col_num, position_exist):
    a = 3
    while True:
        try:
            #set up scraping process
            element = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, "//*[@id='stats-app-root']/div/section/section/div[3]/div[2]/div/div/div[3]/button")))
            element.click()
            time.sleep(20)

            #scraping part
            length_of_player = scrape_player_posit(name_list, position_list, browser, position_exist)
            scrape_stats(length_of_player, big_list, browser, col_num)
            print("page " + str(a) + ":")
            print("scrape " + str(length_of_player) + " rows")
            print("Total row: " + str(len(name_list)))
            #increment page num
            a = a + 1

        except TimeoutException:
            print("Time out exception! ")
            break
    print("scrape ends")

def scrape_mlb(year, browser, name_list, position_list, big_list, col_num, position_exist, url_path):
    # Establish chrome driver and go to report site URL
    print("process year " + str(year))
    browser.get(url_path)
    time.sleep(15)

    #accept the website cookie
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))).click()
    except TimeoutException:
        pass

    time.sleep(15)

    # #scrape the first page
    length_n_player = scrape_player_posit(name_list, position_list, browser, position_exist)
    scrape_stats(length_n_player, big_list, browser, col_num)
    print("page 1: ")
    print("scrape " + str(length_n_player) + " rows")
    print("Total row: " + str(len(name_list)))

    # go to the second page first since html/css different
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='stats-app-root']/div/section/section/div[3]/div[2]/div/div/div[2]/button"))).click()

    time.sleep(15)
    length_of_player = scrape_player_posit(name_list, position_list, browser, position_exist)
    scrape_stats(length_of_player, big_list, browser, col_num)
    print("page 2: ")
    print("scrape " + str(length_of_player) + " rows")
    print("Total row: " + str(len(name_list)))

    # #automate the scraping part
    auto_scrape(name_list, position_list, big_list, browser, col_num, position_exist)

    # merge column
    if position_exist:
        big_list.insert(0, position_list)
    big_list.insert(0, name_list)

def export_csv(big_list, col_name_list, filename):
    data = pd.DataFrame(big_list).transpose()
    data.columns = col_name_list
    file_name = filename
    data.to_csv(file_name, index = False)
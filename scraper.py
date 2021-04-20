from os import execlp
import chromedriver_binary # nopa
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time as t
import json
from tqdm import tqdm
from bs4 import BeautifulSoup
import argparse as ap


f = open('setting.json', 'r')
data = json.load(f)

def get_driver():
    usrif = data["user_info"]
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    profile_path = './UserData'
    options.add_argument('--user-data-dir=' + usrif["profile_path"])
    options.add_argument("--window-size=2048,2048")
    options.add_argument(f"--user-agent={usrif['useragent']}")
    driver = webdriver.Chrome(options=options)
    return driver

def login():
    usrif = data["user_info"]
    pixiv_id = usrif["login"]["id"]
    pixiv_pass = usrif["login"]["password"]
    driver = get_driver()
    
    driver.get("https://accounts.pixiv.net/login")

    t.sleep(1)
    login_id = driver.find_element(By.XPATH,'//*[@id="LoginComponent"]/form/div[1]/div[1]/input')
    action = ActionChains(driver)
    action.click(login_id)
    action.send_keys(pixiv_id)
    action.perform()
    t.sleep(1)
    passward = driver.find_element(By.XPATH,'//*[@id="LoginComponent"]/form/div[1]/div[2]/input')
    action = ActionChains(driver)
    action.click(passward)
    action.send_keys(pixiv_pass)
    action.perform()
    t.sleep(1)
    btn = driver.find_element(By.XPATH, '//*[@id="LoginComponent"]/form/button')
    action = ActionChains(driver)
    action.click(btn)
    action.perform()
    t.sleep(20) # If it is too short, login will fail
    print("Login OK")
    #driver.quit()
    #return driver


def each_user_illust():
    illustrator_id = data["illustrator_id"]
    print("scraping each user illust ...")
    for id in illustrator_id:
        object = f"users/{id}/illustrations"
        print(object)
        scraping(object)

    print("Succeeded")

def each_tag_illust():
    tag_word = data["tag_word"]
    print(f"scraping each tag illust ...")
    for tag in tag_word:
        object = f"tags/{tag}/illustrations"
        print(object)
        scraping(object)

    print("Succeeded") 

def scraping(object):
    n_page = 1
    while True:
        print(f"{n_page} page scraping now...")
        driver = get_driver()
        driver.get(f'https://www.pixiv.net/{object}?p={n_page}')

        html = driver.page_source

        soup = BeautifulSoup(html, "lxml")
    
        linklist = []
        next_link = soup.select("div.rp5asc-0.bscYTy > a")
        print(len(next_link))
        if len(next_link) != 0:
            for l in next_link:
                link = l.attrs["href"]
                linklist.append(link)

            t.sleep(1)
            for l in linklist[:]:
                try:
                    print(f"{l} OK")
                    driver.get("https://www.pixiv.net" + l)
                    t.sleep(10) # The wait time Depends on your network speed. At least 5 seconds is recommended so as not to bother the server.
                    png = driver.find_element_by_class_name('sc-1qpw8k9-1.fvHoJ').screenshot_as_png
                    illustID = l.split("/")[3]
                    with open(f"./images/{illustID}.png", "wb") as f:
                        f.write(png)
                except:
                    print(f"{l} ERROR")
            n_page += 1
        else:
            break

def main():

    parser = ap.ArgumentParser()
    parser.add_argument('mode')
    args = parser.parse_args()
    
    if args.mode == "user":
        each_user_illust()
    elif args.mode == "tag":
        each_tag_illust()


if __name__ == "__main__":
    main()


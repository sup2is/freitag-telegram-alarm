import datetime
import sys
from time import sleep
import threading

import chromedriver_autoinstaller
import redis
import telegram
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def get_new_items(urls, keys, chose_items, idx):
    idx %= len(chose_items)
    itemIdx = int(chose_items[idx])
    try:
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver')
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver')

    driver.get(url=urls[itemIdx])

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                    "#block-freitag-content > article > section:nth-child(2) > div > div > div > div > div > div > div > div > a")))

    click = driver.find_element(By.CSS_SELECTOR,
                                '#block-freitag-content > article > section:nth-child(2) > div > div > div > div > div > div > div > div > a')
    driver.execute_script("arguments[0].click();", click)

    elements = driver.find_elements(By.CSS_SELECTOR, 'section.layout picture img');

    count = 0

    for item in elements:
        image_src = item.get_attribute('src')
        alt = item.get_attribute(':alt')

        if alt is not None and not redis.exists(keys[itemIdx] + ":" + image_src):
            redis.set(
                keys[itemIdx] + ":" + image_src,
                image_src,
                datetime.timedelta(days=30)
            )
            bot.sendMessage(chat_id=user_id, text=image_src)
            count += 1

        sleep(1)

    print("new ({}) count : {}".format(keys[itemIdx], count))
    threading.Timer(1200, get_new_items, [urls, keys, chose_items, idx + 1]).start() # 20분간격으로 번갈아가면서 동작

if __name__ == '__main__':

    my_token = "" # telegram 토큰입력
    user_id = "" # telegram user_id 입력
    bot = telegram.Bot(token=my_token)
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인
    redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    dict = {"miami": "https://www.freitag.ch/en/f52",
           "dragnet": "https://www.freitag.ch/en/f12",
           "lassie": "https://www.freitag.ch/en/f11",
           "dexter": "https://www.freitag.ch/en/f14",
           "leland": "https://www.freitag.ch/en/f202",
           "bob": "https://www.freitag.ch/en/f203"}

    print("\n****\nChoose two \nexample: 1 2 or 2 5 or 3 3\n****\n")

    for idx, item in enumerate(dict):
        print(str(idx) + ": " + item)

    chose_items = input().split()

    keys = list(dict.keys())
    urls = list(dict.values())

    print("chose item: {}, {}".format(keys[int(chose_items[0])], keys[int(chose_items[1])]))
    print("It runs every 30 minutes.")
    get_new_items(urls, keys, chose_items, 0)



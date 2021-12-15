import datetime
import subprocess
import sys
from time import sleep

import chromedriver_autoinstaller
import redis
import telegram
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

product_name = sys.argv[1]
print("### product_name : " +  product_name);
my_token = ""
user_id = ""
bot = telegram.Bot(token = my_token)
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

subprocess.Popen(r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~\chrometemp"', shell=True)

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver', options=option)

URL = 'https://www.freitag.ch/en/f52'

driver.get(url=URL)

picture = WebDriverWait(driver, 5000).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#block-freitag-content > article > section:nth-child(2) > div > div > div > div > div > div > div > div > a")))

click = driver.find_element(By.CSS_SELECTOR, '#block-freitag-content > article > section:nth-child(2) > div > div > div > div > div > div > div > div > a')
driver.execute_script("arguments[0].click();", click)

elements = driver.find_elements(By.CSS_SELECTOR, 'section.layout picture img');

for item in elements:
    image_src = item.get_attribute('src')
    alt = item.get_attribute(':alt')

    if alt is not None and not redis.exists(product_name + ":" + image_src):
        sleep(0.5)
        redis.set(
            product_name + ":" + image_src,
            image_src,
            datetime.timedelta(days=30)
        )
        bot.sendMessage(chat_id=user_id, text=image_src)


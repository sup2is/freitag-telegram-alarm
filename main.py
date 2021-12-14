from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import redis

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver')
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver')

driver.implicitly_wait(30)

URL = 'https://www.freitag.ch/en/f52'
# URL = 'https://www.naver.com'

driver.get(url=URL)

curr_items = []
new_items = []

for item in driver.find_elements(By.CSS_SELECTOR, 'section.layout picture img'):
    image_src = item.get_attribute('src')
    alt = item.get_attribute(':alt')

    if alt is not None:
        redis.sadd("miami", image_src)



if __name__ == "__main__":
    print("test")
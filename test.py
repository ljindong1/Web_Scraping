import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


# 식당 url 얻기
options = webdriver.ChromeOptions()
# 브라우저 로깅을 비활성화
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# URL 정의
url = "https://map.naver.com/v5/search/%EC%A4%91%ED%99%94%EB%A1%9C/place/1026712515?c=15,0,0,0,dh&placePath=%3Fentry%253Dbmp"

# 검색 url 접속 = 검색하기
driver.get(url)  

time.sleep(3)

# 검색 프레임 변경
iframe = driver.find_element(By.ID, "entryIframe")
driver.switch_to.frame(iframe)

naver_name = driver.find_element(By.CLASS_NAME, "Fc1rA")
# # naver_name = soup.find_element(By.CLASS_NAME, "place_bluelink").get_text()
print(naver_name.text)

input("next?") + ' '



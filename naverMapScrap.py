import pandas as pd
import openpyxl
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from pyparsing import col
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm 
import re
import pyproj

# UTM 좌표계 정보
utm_zone = 51
south_hemisphere = False
utm_proj = pyproj.Proj(proj='utm', zone=utm_zone, south=south_hemisphere)


def checkIsList():
    try:
        WebDriverWait(driver, 3).until(EC.visibility_of(driver.find_element(By.ID, "searchIframe"))) 
        return True
    except Exception as e:
        return False
        #검색결과가 없을때

def switch_iframe(iframeID):
    driver.switch_to.default_content()  # frame 초기화
    iframe = driver.find_element(By.ID, iframeID)
    driver.switch_to.frame(iframe)
    time.sleep(1)


def scrapeData(url):
    driver.get(url)
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "share-url-button > #spiButton_share_map")))
    data_url = element.get_attribute('data-url')
    pattern = r"(\d+\.\d+),(\d+\.\d+)"
    match = re.search(pattern, data_url)
    if match:
        latitude, longitude  = match.groups()       
    else:
        latitude, longitude = ""

   
    entry_iframe = driver.find_element(By.ID, "entryIframe")
    driver.switch_to.frame(entry_iframe)

    time.sleep(1)

    cafename = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Fc1rA")))
    cafeAddr = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "LDgIH")))  

    return cafename.text, cafeAddr.text , latitude, longitude 

#################################################################################################################

restaurant = pd.read_csv('양천구_음식점_20220930.csv', encoding='cp949')
names = restaurant['업소명']

df = pd.DataFrame(columns=['name', 'naverURL'])
df['name'] = names


# 식당 url 얻기
options = webdriver.ChromeOptions()
# 브라우저 로깅을 비활성화
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()

driver.implicitly_wait(10) 

for i, keyword in enumerate(df['name'].tolist()):
    if i == 6: 
        break
    
    print(f"====={keyword}=====================================")
    # 검색 url 만들기
    url = f'https://map.naver.com/v5/search/{keyword}/place'  
    # url = f'https://map.naver.com/v5/search/손오공마라탕 목동점/place'  

    # 검색 url 접속 = 검색하기
    driver.get(url)  

    if checkIsList():
        # 검색 프레임 변경
        switch_iframe(iframeID="searchIframe")

        # searched_list = driver.find_elements(By.CSS_SELECTOR, ".VLTHu.OW9LQ")
        element = driver.find_element(By.CSS_SELECTOR, "span.place_bluelink")  # place_bluelink TYaxT  .place_bluelink.YwYLL
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element))
        element.click()

        # 새로운 페이지로 이동하여 새로운 정보 가져오기
        driver.get(driver.current_url)

        switch_iframe(iframeID="searchIframe")
        searched_list = driver.find_elements(By.TAG_NAME,  "li") # ".VLTHu.OW9LQ", ".UEzoS.rTjJo"
        searchCount = len(searched_list)
        if searchCount > 5: 
            searchCount = 5

        for j in range(searchCount):
            switch_iframe(iframeID="searchIframe")
            element = driver.find_elements(By.CSS_SELECTOR, "span.place_bluelink")[j].click()

            cafename, cafeAddr, latitude, longitude = scrapeData(driver.current_url)
            print(f'{cafename} : {cafeAddr} : {latitude, longitude}')

    else:
        cafename, cafeAddr, latitude, longitude = scrapeData(driver.current_url)
        print(f'{cafename} : {cafeAddr} : {latitude, longitude}')

        # time.sleep(1)
        # input("next?") + ' '
    time.sleep(5)
    
driver.close()


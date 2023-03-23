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

def checkIsList():
    try:
        WebDriverWait(driver, 3).until(EC.visibility_of(driver.find_element(By.ID, "searchIframe")))   
        print("TRUE")
        # driver.switch_to.default_content()
        # search_iframe = driver.find_element(By.ID, "searchIframe")
        # driver.switch_to.frame(search_iframe)
        # element = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID, "_pcmap_list_scroll_container")))
        # print(element)
        # driver.switch_to.default_content()
        return True
    except Exception as e:
        print("False")
        return False
        #검색결과가 없을때

def switch_iframe(iframeID):
    driver.switch_to.default_content()  # frame 초기화
    iframe = driver.find_element(By.ID, iframeID)
    driver.switch_to.frame(iframe)
    time.sleep(1)


def scrapeData(url):
    driver.get(url)
    entry_iframe = driver.find_element(By.ID, "entryIframe")
    driver.switch_to.frame(entry_iframe)

    time.sleep(1)

    cafename = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "Fc1rA")))
    cafeAddr = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "LDgIH")))  

    return cafename.text, cafeAddr.text  

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
            cafename, cafeAddr = scrapeData(driver.current_url)
            print(f'{cafename} : {cafeAddr}')

    else:
        cafename, cafeAddr = scrapeData(driver.current_url)
        print(f'{cafename} : {cafeAddr}')

        # time.sleep(1)
        # input("next?") + ' '
    time.sleep(5)
    
driver.close()

sys.exit()

#식당명과 url이 잘 얻어져왔는지 확인하기
print(df)

#url을 얻어오지 못한 식당 확인
print(df.loc[df['naverURL']==''])
#결측치로 입력된 식당 확인
print(df.loc[df['naverURL'].isna()])
## 식당 리뷰 url이 들어가있지 않은 경우 직접 검색하여 데이터에 넣어주기!!! ##

# csv 파일로도 저장하여 url이 빈 값이 있는지 반드시 확인할 것 !
#url이 없으면 코드 실행이 중단되므로 반드시 url 데이터를 확인할 것!!
df.to_csv('마포구url.csv', encoding='utf-8-sig')

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.maximize_window()


count = 0 #
current = 0 #현재 진행 상황

goal = len(df['name']) #총 식당 수

#데이터 프레임으로 만들 빈 리스트 생성
rev_list=[]


for i in range(len(df)): 
    
    current += 1
    print('진행상황 : ', current,'/',goal,sep="")
    
    
    # 식당 리뷰 개별 url 접속
    driver.get(df['naverURL'][i]) 
    thisurl = df['naverURL'][i]
    time.sleep(2)
    print('현재 수집중인 식당 : ', df['name'][i])
    
    #리뷰 더보기 버튼 누르기
    while True: 
        try:
            driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div:nth-child(7) > div:nth-child(2) > div.place_section.lcndr > div.lfH3O > a')
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(1)
            driver.execute_script('return document.querySelector("#app-root > div > div > div > div:nth-child(7) > div:nth-child(2) > div.place_section.lcndr > div.lfH3O > a").click()')
            time.sleep(2) 
                        
        except NoSuchElementException:
            print("-모든 리뷰 더보기 완료-")
            break    
        
    #식당 평균 별점 수집
    try:
        rating = driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div:nth-child(7) > div:nth-child(2) > div.place_section.no_margin.mdJ86 > div.place_section_content > div > div.Xj_yJ > span.m7jAR.ohonc > em').text
        print('식당 평균 별점 : ', rating)
        rev_list.append(
            [df['name'][i],
             rating
             ]
        )
    except:
        pass
    
    

     
        
    #리뷰 데이터 스크래핑을 위한 html 파싱
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        #키워드 리뷰가 아닌 리뷰글 리스트 검색
        review_lists = soup.select('#app-root > div > div > div > div:nth-child(7) > div:nth-child(2) > div.place_section.lcndr > div.place_section_content > ul > li')
        
        print('총 리뷰 수 : ', len(review_lists))
        
        #리뷰 수가 0이 아닌 경우 리뷰 수집
        if len(review_lists) > 0 :
            
            for j, review in enumerate(review_lists):
                
                try:
                    
                    #내용 더보기가 있는 경우 내용 더보기를 눌러주기
                    try:
                        review.find(' div.ZZ4OK > a > span.rvCSr > svg')
                        more_content = review.select(' div.ZZ4OK > a > span.rvCSr > svg')
                        more_content.click()
                        time.sleep(1)
   
                        #리뷰 정보
                        user_review = review.select(' div.ZZ4OK > a > span')
                           
                
                        #리뷰 정보가 있는 경우 식당 이름, 평점, 리뷰 텍스트, 작성 시간을 가져와서 데이터 프레임으로 만들기
                        if len(user_review) > 0:
                             rev_list.append(
                                [
                                    df['name'][i],
                                    '',
                                    user_review[0].text
                                ]
                                )      
                       
                        time.sleep(1)            
                
                    
                    
                    except:
                        #리뷰 정보
                        user_review = review.select(' div.ZZ4OK.IwhtZ > a > span')
                        
        
                        #리뷰 정보가 있는 경우 식당 이름, 평점, 리뷰 텍스트, 작성 시간을 가져와서 데이터 프레임으로 만들기
                        if len(user_review) > 0:
                            rev_list.append(
                                [
                                    df['name'][i],
                                    '',
                                    user_review[0].text
                                ]
                                )      
                        
                        time.sleep(1) 
                        
                except NoSuchElementException:
                    print('리뷰 텍스트가 인식되지 않음')
                    continue  
                
        else:
            print('리뷰 선택자가 인식되지 않음')
            time.sleep(1)                
        
       
        


    # 리뷰가 없는 경우        
    except NoSuchElementException: 
               
        rev_list.append(
        [
            df['name'][i],
            rating,
        ]
        ) 
        time.sleep(2)           
        print("리뷰가 존재하지 않음")

    
            
    #검색한 창 닫고 검색 페이지로 돌아가기    
    # driver.close()
    # driver.switch_to.window(tabs[0])
    print("기본 페이지로 돌아가기")

        
driver.close()

#스크래핑한 데이터를 데이터 프레임으로 만들기  
column = ["name", 'rate', "review"]
df2 = pd.DataFrame(rev_list, columns=column)
df2   
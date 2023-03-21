import selenium #셀레니움
import pandas as pd #csv를 읽고 dataframe을 사용하기 위한 pandas
from selenium import webdriver #브라우저를 띄우고 컨트롤하기 위한 webdriver
from selenium.webdriver.common.keys import Keys #브라우저에 키입력 용
from selenium.webdriver.common.by import By #webdriver를 이용해 태그를 찾기 위함
from selenium.webdriver.support.ui import WebDriverWait #Explicitly wait을 위함
from webdriver_manager.chrome import ChromeDriverManager #크롬에서 크롤링 진행 크롬 웹 드라이버 설치시 필요
from selenium.webdriver.support import expected_conditions as EC #브라우저에 특정 요소 상태 확인을 위해
from bs4 import BeautifulSoup #브라우저 태그를 가져오고 파싱하기 위함
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException #예외처리를 위한 예외들 

def checkIsList(checkCount):
    try:
        driver.switch_to.default_content()
        WebDriverWait(driver,1.5).until(
        EC.presence_of_element_located((By.ID, searchFrame))
        )
        driver.switch_to.frame(searchFrame)    
        WebDriverWait(driver,1).until(
            EC.presence_of_element_located((By.CLASS_NAME, resultListTitleClass))
        )
        driver.switch_to.default_content()
        return 0;
    except TimeoutException:
        #검색결과 바로 식당정보로 이동했을때
        try:
            driver.switch_to.default_content()
            WebDriverWait(driver,1.5).until(
            EC.presence_of_element_located((By.ID, entryFrame))
            )
            driver.switch_to.frame(entryFrame)
            WebDriverWait(driver,1).until(
                EC.presence_of_element_located((By.CLASS_NAME, resultTargetTitleDiv))
            )
            driver.switch_to.default_content()
            return 1
        #검색결과가 없을때
        except TimeoutException:
            
            #처음이면 검색어를 다시 구성해서 검색
            if(checkCount==0):
                return 2
            #검색어를 다시 구성했는데도 없으면 없는가게
            elif(checkCount==1):
                return 3


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://map.naver.com/v5/")
try:
   element = WebDriverWait(driver, 10).until(
       EC.presence_of_element_located((By.CLASS_NAME, "input_search"))
   ) #입력창이 뜰 때까지 대기
finally:
   pass

keyword = input("찾고자 하시는 명칭을 입력하시오:")

search_box = driver.find_element(By.CLASS_NAME,"input_search")
search_box.send_keys(keyword)
search_box.send_keys(Keys.ENTER)

for i in range(2):     
            search(flag)
            checkResult = checkIsList(i)
            if checkResult == 0:   #결과가 리스트로 나옴
                #todo
                #맞는지 검사하고 맞으면 크롤링 진행, 틀리면 
                #선택하고
                driver.switch_to.default_content()
                driver.switch_to.frame(searchFrame)
                #driver.find_element(By.CSS_SELECTOR,resultTitleClick).click()
                driver.find_element(By.CSS_SELECTOR,resultTitleClick).send_keys(Keys.ENTER)
                driver.switch_to.default_content()
                WebDriverWait(driver,4).until(
                EC.presence_of_element_located((By.ID, entryFrame))
                )
                driver.switch_to.frame(entryFrame)
                getInfo(row)
                driver.switch_to.default_content()
                break
            elif checkResult ==1:  #결과가 바로 식당정보로 나옴
                #바로 정보뽑기
                driver.switch_to.default_content()
                WebDriverWait(driver,4).until(
                    EC.presence_of_element_located((By.ID, entryFrame))
                )
                driver.switch_to.frame(entryFrame)
                getInfo(row)
                break
            elif checkResult ==2:  #처음인데 결과가 안나옴
                flag = False
                continue
            elif checkResult ==3: #두번째인데도 결과가 안나옴
                data.loc[idx,"리뷰"] = "noResult"
                # print(str(idx) + ". "+ data.loc[idx,"상호명"]+" 
                      
driver.find_element(By.CLASS_NAME,"button_clear").send_keys(Keys.ENTER)
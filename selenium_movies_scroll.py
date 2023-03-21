import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup

browser = webdriver.Chrome()
browser.maximize_window()

url = "https://play.google.com/store/movies/category/MOVIE?hl=ko"
browser.get(url)

# 스크롤 내리기
# browser.execute_script("window.scrollTo(0, 1080)")

# 화면 가장 아래로 스크롤 내리기
browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
interval = 2

prev__height = browser.execute_script("return document.body.scrollHeight")

while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(interval)

    curr_height = browser.execute_script("return document.body.scrollHeight")
    if curr_height == prev__height:
        break

    prev__height = curr_height


soup = BeautifulSoup(browser.page_source, "lxml")

movies = soup.find_all("div", attrs={"class":"VfPpkd-WsjYwc"})
print(len(movies))

for movie in movies:
#     # print("-"*50)
#     # print(movie)
    title = movie.find("div", attrs={"class":"hP61id"}).get_text()

    # price = movie.find("span", attrs={"class":""})

    # link = movie.find("a", attrs={"class":""})["href"]
    print("https://play.google.com" + link)
    print(title)

browser.quit()
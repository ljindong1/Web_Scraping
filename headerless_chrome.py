import time
from selenium import webdriver

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")

browser = webdriver.Chrome(options=options)
browser.maximize_window()

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


browser.get_screenshot_as_file("google_movie.png")
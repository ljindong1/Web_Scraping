
import time
from selenium import webdriver

browser = webdriver.Chrome() # "./chromedriver.exe"

browser.get("http://naver.com")

elem = browser.find_element_by_class_name("link_login")
elem.click()

browser.find_element_by_id("id").send_keys("ljindong1986")
browser.find_element_by_id("pw").send_keys("King0218")

browser.find_element_by_id("log.login").click()

time.sleep(3)

# browser.find_element_by_id("id").clear()
# browser.find_element_by_id("id").send_keys("my_id")

print(browser.page_source)

# browser.close()
browser.quit()

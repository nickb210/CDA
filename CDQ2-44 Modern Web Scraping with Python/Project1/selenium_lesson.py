#!/usr/bin/env python3
import requests, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

CHROME_PATH = '/Users/nicholausbrell/python/selenium/chromedriver'
URL = 'https://www.google.com/'

chrome_options = Options()
chrome_options.headless = True

driver = webdriver.Chrome(CHROME_PATH)
driver.get(URL)
time.sleep(3)

search = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
search.send_keys('san antonio')
search.send_keys(Keys.ENTER)
#driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]').click()

time.sleep(3)
driver.quit()
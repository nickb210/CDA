#!/usr/bin/env python3
import requests, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

"""
RETRUN THE FOLLOWING:
    - # of courses, total time, # of case studies
    - text from market and career opportunity
    - instructor list
"""

CHROME_PATH = '/Users/nicholausbrell/python/selenium/chromedriver'
URL = 'https://sdsclub.com/'

# create a driver 
driver = webdriver.Chrome(CHROME_PATH)

# go to URL
driver.get(URL)
time.sleep(2) # sleep for 2 seconds so page can load

driver.find_element_by_xpath('//*[@id="menu-item-456"]/a').click()
time.sleep(2) # sleep for 2 seconds so page can load

driver.find_element_by_xpath('//*[@id="category-career"]/div/div[2]/div[4]/div/figure/a/img').click()
time.sleep(2) # sleep for 2 seconds so page can load

# get the page source in order to create a BS object to parse
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml') # create BS object to parse
driver.quit() # close the chrome browser since its no longer needed 

# list created to store # of courses, total time, # of case studies
lifetime_access = soup.find_all('span', class_='desc')
for i in lifetime_access:
    print(str(i.text).strip())

# list created to store text from market and career opportunity
ops = soup.find('div', class_='single-path-articles')
print("\n")

# loop to iterate through the 'ops' list and find all the text by class name 
for i in ops.find_all('div', class_='single-path-article-content'):
    print(str(i.text).strip() + "\n")

# list to store instructors for the course
instructors = soup.find_all('p', class_='name')
for i in instructors:
    print(i.text)

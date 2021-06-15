#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import pandas
import time

"""
Challenge:
Retreive the number of reviews for each item on Amazon's
best seller page. *BONUS* Put the numbers in a data frame.
"""
URL = 'https://www.amazon.com/Best-Sellers/zgbs'

# https://www.networkinghowtos.com/howto/common-user-agent-list/
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

# make the GET request using the headers defined in the 'header' variable
r = requests.get(URL, headers=header)

# create BS object to parse
soup = BeautifulSoup(r.content, 'lxml')

# retrieve the total product reviews by class name
product_reviews = soup.find_all('a', class_='a-size-small a-link-normal')

# create list for dataframe
rev_list = []

# loop to add values from 'product_reviews' into the 'rev_list' variable
# which will be used to create the dataframe
for review in product_reviews:
    rev_list.append(review.text) # add values to list

# create data frame from list
df = pandas.DataFrame(rev_list)
print(df)


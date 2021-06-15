#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

r = requests.get('https://quotes.toscrape.com/')

soup = BeautifulSoup(r.content, 'lxml')

quotes = soup.find_all('div', class_='quote')


for i in quotes:
    tags_list = []
    text = i.find('span', class_='text').text
    tags = i.find_all('a', class_='tag')
    
    for t in tags:
        #print(t.text)
        tags_list.append(t.text)

    print(text)
    print(tags_list)
    print("\n")
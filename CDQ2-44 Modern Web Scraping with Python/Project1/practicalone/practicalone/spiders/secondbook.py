#!/usr/bin/env python3

import scrapy
from practicalone.items import PracticaloneItem

"""
Scenario:
    You want to scrape the following webpage becuase you want to
    pay attention to the price information from the books to scrape.
    Furthermore you want to check one specific book
"""

class secondSpider(scrapy.Spider):
    name = "Books2"
    start_urls = [
        "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
    ]

    def parse(self, response):
        item = PracticaloneItem()
        item['title'] = response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/h1').extract()
        item['price'] = response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/p[1]').extract()
        #item['price'] = response.xpath("//p[@class='price_color']/text()").get()

        return item
    
#!/usr/bin/env python3
import scrapy
from practicalone.items import PracticaloneItem

"""
Challange:
    Get the title, price, category and stock of 4 different books.
"""

class sectionThreeChallenge(scrapy.Spider):
    name = "Challenge1"
    start_urls = [
        "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
        "https://books.toscrape.com/catalogue/soumission_998/index.html",
        "https://books.toscrape.com/catalogue/sharp-objects_997/index.html"
    ]

    def parse(self, response):
        item  = PracticaloneItem()

        #item['title'] = response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/h1').extract()
        item['title'] = response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get()

        #item['price'] = response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/p[1]').extract()
        item['price'] = response.xpath("//div[@class='col-sm-6 product_main']/p/text()").get()

        #item['category'] = response.xpath('//*[@id="default"]/div/div/ul/li[3]/a').extract()
        item['category'] = response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get()
        
        #item['stock'] = response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/p[2]').extract()
        item['stock'] = response.xpath("normalize-space(//p[@class='instock availability']/i/following::node()[1])").get()

        return item

#!/usr/bin/env python3

# section 1
import scrapy

# section 2
# http://books.toscrape.com/catalogue/category/books/science_22/index.html
class firstspider(scrapy.Spider):
    # $: scrapy crawl Books
    name = "Books"
    
    # target URL's
    start_urls = [
     "https://books.toscrape.com",
     "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
     ]
    
    
    # section 3
    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'books-%s.html' % page
        f = open(filename, "wb")
        f.write(response.body)
        f.close()
        
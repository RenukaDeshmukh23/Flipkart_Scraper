# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy import Selector
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException

class ElectronicsSpider(scrapy.Spider):
    name = 'electronics'
    allowed_domains = ['flipkart.com']
    #start_urls = ['https://www.flipkart.com/search?q=mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off']
    def start_requests(self):
        self.driver = webdriver.Chrome('F:/chromedriver')
        self.driver.get('https://www.flipkart.com/search?q=mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off')
        self.driver.maximize_window()
        sleep(5)

    #def parse(self, response):
        response = Selector(text=self.driver.page_source)
        URLs=response.xpath('//*[@class="s1Q9rs"]//@href').extract()
        for URL in URLs:
            absolute_URL="https://www.flipkart.com"+URL
            #print("-------",absolute_URL,"-------")
            #yield{'url':absolute_URL}
            yield Request(absolute_URL,callback=self.parse_products)
        for i in range (2,10000):
            Next="https://www.flipkart.com/search?q=mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="+(str(i))
            self.driver.get(Next)
            if Next:
            #print("Next page=",Next)
                response = Selector(text=self.driver.page_source)
                URLs=response.xpath('//*[@class="s1Q9rs"]//@href').extract()
                for URL in URLs:
                    absolute_URL="https://www.flipkart.com"+URL
                    #print("-------",absolute_URL,"-------")
                    #yield{'url':absolute_URL}
                    yield Request(absolute_URL,callback=self.parse_products)
            else:
                print('No more pages to load.')
                self.driver.quit()
            #yield Request(Next,callback=self.parse_products)
    def parse_products(self,response):
        name=response.xpath('//*[@class="yhB1nd"]//text()').extract_first()
        price=response.xpath('//*[@class="_30jeq3 _16Jk6d"]//text()').extract_first()
        yield{'name':name,
            'Price':price}

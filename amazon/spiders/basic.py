# -*- coding: utf-8 -*-
import scrapy
import json

class BasicSpider(scrapy.Spider):
    name = 'basic'
    crawlera_enabled = True
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def start_requests(self):
        urls=['https://httpbin.org/ip', 'https://httpbin.org/user-agent']
        for url in urls:
            request = scrapy.Request(url)
            yield request


    def parse(self, response):
        item = json.loads(response.text)
        yield item

# -*- coding: utf-8 -*-
import scrapy


class MwsXsdSpider(scrapy.Spider):
    name = 'mws-xsd'
    allowed_domains = ['web']
    start_urls = ['http://web/']

    def parse(self, response):
        pass

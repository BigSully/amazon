# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from io import BytesIO

class MwsXsdSpider(scrapy.Spider):
    name = 'mws-xsd'
    allowed_domains = ['docs.developer.amazonservices.com', 'images-na.ssl-images-amazon.com', 's3.amazonaws.com', 'amazonaws.com']

    def start_requests(self):
        urls=['http://docs.developer.amazonservices.com/en_UK/feeds/Feeds_SubmitFeed.html']
        for url in urls:
            request = scrapy.Request(url)
            yield request

    def parse(self, response):
        for link in response.xpath('//a/@href').extract():
            if link.endswith('.xsd') or link.endswith('.xls') or link.endswith('.pdf'):
                yield scrapy.Request(url=response.urljoin(link), callback=self.save_file)
            else:
                yield scrapy.Request(url=response.urljoin(link), callback=self.parse)

    def save_file(self, response):
        path = "{}/{}".format(self.settings['AMAZON_FILES'], response.url.split('/')[-1])
        with open(path, 'wb') as f:
            f.write(response.body)

        url=response.request.url
        if url.endswith('.xsd'):
            yield { "url": url, "data": response.body }

            ## xsd file may refer to other xsd files
            tree = etree.parse(BytesIO(response.body))
            namespaces = {'xsd': 'http://www.w3.org/2001/XMLSchema'}
            r = tree.xpath('/xsd:schema/xsd:include', namespaces=namespaces)
            for elem in r:
                xsd_name = elem.attrib['schemaLocation']
                yield scrapy.Request(url=response.urljoin(xsd_name), callback=self.save_file)


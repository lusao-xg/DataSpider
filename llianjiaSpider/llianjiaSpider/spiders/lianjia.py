# -*- coding: utf-8 -*-
import scrapy
from ..items import LlianjiaspiderItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    n = 100
    start_urls = ['https://bj.lianjia.com/ershoufang/pg{}'.format(i) for i in range(1, n+1)]

    def parse(self, response):
        sellList = response.css('.sellListContent li > a::attr(href)')
        for url in sellList:
            yield scrapy.Request(url.get(), callback=self.detail)

    def detail(self, response):
        item = LlianjiaspiderItem()
        item['area'] = ''.join(response.css('.area .mainInfo::text').getall())
        item['price'] = ''.join([response.css('.total::text').get(), response.css('.unit span::text').get()])
        item['pattern'] = response.css('.room .mainInfo::text').get()
        item['floor'] = response.css('.room .subInfo::text').get()
        item['toward'] = response.css('.type .mainInfo::text').get()
        item['decorationor'] = response.css('.type .subInfo::text').get()
        item['construction'], item['floor_type'] = response.css('.area .subInfo::text').get().split('/')
        item['region'] = ' '.join(response.css('.areaName *::text').getall()[1:]).replace('\xa0', '')
        item['hasElevator'] = response.css('.base .content li:last-child::text').get()
        item['year_limit'] = response.css('.transaction .content li:nth-child(5) span:last-child::text').get()
        item['authority'] = response.css('.transaction .content li:nth-child(2) span:last-child::text').get()
        item['roomType'] = response.css('.base .content li:first-child::text').get()
        yield item

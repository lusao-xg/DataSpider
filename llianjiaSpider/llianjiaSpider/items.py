# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LlianjiaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    pattern = scrapy.Field()
    floor = scrapy.Field()
    toward = scrapy.Field()
    decorationor = scrapy.Field()
    construction = scrapy.Field()
    floor_type = scrapy.Field()
    region = scrapy.Field()
    hasElevator = scrapy.Field()
    year_limit = scrapy.Field()
    authority = scrapy.Field()
    roomType = scrapy.Field()

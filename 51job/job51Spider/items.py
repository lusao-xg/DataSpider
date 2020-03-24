# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Job51SpiderItem(scrapy.Item):
    # 职位名称
    jobName = scrapy.Field()
    # 薪资
    salary = scrapy.Field()
    # 工作经验
    needWorkExperience = scrapy.Field()
    # 学历
    education = scrapy.Field()
    # 公司地址
    companyAdder = scrapy.Field()
    # 职位描述
    description = scrapy.Field()
    # 任职要求
    jobRequire = scrapy.Field()
    # 公司所属行业
    companyType = scrapy.Field()
    # 公司人数
    employeeNum = scrapy.Field()
    # 职位链接
    jobUrl = scrapy.Field()

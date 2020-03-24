# -*- coding: utf-8 -*-
import re

import scrapy
from ..items import Job51SpiderItem


class Job51Spider(scrapy.Spider):
    name = 'job51'
    allowed_domains = ['51job.com']

    # 地区码
    areaCode = ['010000']
    # 需要采集关键字
    searchWords = ['java']

    # 构造请求链接
    def start_requests(self):
        for area in self.areaCode:
            for word in self.searchWords:
                url = 'https://search.51job.com/list/%s,000000,0000,00,9,99,%s,2,1.html' % (area, word)
                yield scrapy.Request(url)

    # 解析每个职业的链接
    def parse(self, response):
        links = response.css('div.el .t1 a::attr(href)').getall()
        for url in links:
            yield scrapy.Request(url, callback=self.parseDetail)
        # 判断是否存在下一页
        hasNext = response.css('.bk:last-child a::attr(href)')
        if hasNext:
            yield scrapy.Request(hasNext.get())

    # 获取招聘详细信息
    def parseDetail(self, response):

        item = Job51SpiderItem()
        # 职位名称
        item['jobName'] = response.css('h1::attr(title)').get()
        # 薪资
        item['salary'] = '未知' if not response.css('.cn strong::text').get() else response.css('.cn strong::text').get()
        # 工作经验
        item['needWorkExperience'] = '无要求' if not response.css('.msg::attr(title)').re('(\d-\d年经验|\d年经验)') else ''.join(
            response.css('.msg::attr(title)').re('(\d-\d年经验|\d年经验)'))
        # 学历
        item['education'] = '无要求' if not response.css('.msg::attr(title)').re('(本科|[硕博]士|大专|在校生/应届生)') else ''.join(
            response.css('.msg::attr(title)').re('(本科|[硕博]士|大专)'))
        # 公司地址
        item['companyAdder'] = '未填写' if not response.css(
            'div.tCompany_main > div:nth-child(2) > div > p::text').get() else response.css(
            'div.tCompany_main > div:nth-child(2) > div > p::text').get()
        # 职位描述
        desc = '\n'.join([des.strip() for des in response.css(".job_msg *::text").getall()[:-6] if '\r\n' not in des])
        key = re.findall('\S\S要求', desc)
        if not key:
            key = '任职资格'
        else:
            key = key[0]
        if key not in desc:
            item['description'] = desc
            item['jobRequire'] = desc
        else:
            item['description'] = desc.split(key)[0]
            # 任职要求
            item['jobRequire'] = desc.split(key)[1]

        # 公司所属行业
        item['companyType'] = response.css('.com_tag .at:last-child::attr(title)').get()
        # 公司人数
        item['employeeNum'] = '未知' if not response.css('.com_tag .at:nth-child(2)::attr(title)').get() else response.css('.com_tag .at:nth-child(2)::attr(title)').get()
        # 职位链接
        item['jobUrl'] = response.url
        yield item

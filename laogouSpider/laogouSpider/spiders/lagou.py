# -*- coding: utf-8 -*-
import json

import requests
import scrapy

headers = {
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}


def get_cookies():
    cookie = requests.get("https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
                          headers=headers, allow_redirects=False).cookies
    return cookie.get_dict()


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    formdata = {'first': 'false',
                'pn': '1',
                'kd': 'python'}

    # start_urls = ['']
    def start_requests(self):
        yield scrapy.FormRequest(self.url, formdata=self.formdata)

    def parse(self, response):
        print(response.request.cookies)
        data = json.loads(response.text)
        showId = data['content']['showId']
        datas = data['content']['positionResult']['result']
        for dat in datas:
            yield dat
        self.formdata['sid'] = showId
        self.formdata['pn'] = str(int(self.formdata['pn']) + 1)
        yield scrapy.FormRequest(self.url, formdata=self.formdata)

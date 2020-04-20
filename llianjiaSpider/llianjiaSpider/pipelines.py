# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class LlianjiaspiderPipeline(object):
    def __init__(self):
        self.csv_file = open('data.csv', 'w', encoding='utf-8', newline='')
        names = ['面积', '价格', '格局', '楼层', '朝向', '装修', '年建', '板楼塔楼', '所在区域', '电梯有无', '房屋年限', '交易权限', '房型']
        self.writer = csv.writer(self.csv_file)
        self.writer.writerow(names)

    def process_item(self, item, spider):
        self.writer.writerow(dict(item).values())
        return item

    def close_spider(self, spider):
        self.csv_file.close()

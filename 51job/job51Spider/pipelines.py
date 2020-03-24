# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from pymysql import Connect


# mysql数据库
class Job51SpiderMysql(object):
    def __init__(self, host, database, port, user, password, table_name):
        self.host = host
        self.database = database
        self.table_name = table_name
        self.user = user
        self.port = port
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            port=crawler.settings.get('MYSQL_PORT'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            table_name=crawler.settings.get('MYSQL_TABLE_NAME'),

        )

    def open_spider(self, spider):
        self.db = Connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            charset='utf8',
        )
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['\"%s\"' % i for i in data.values()])
        sql = "insert into %s(%s) values(%s)" % (self.table_name, keys, values)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()


# MongoDB数据库
class Job51SpiderMongoDB(object):

    def __init__(self, mongodb_url, mongodb_db, mongodb_table_name):
        self.mongodb_url = mongodb_url
        self.mongodb_db = mongodb_db
        self.table_name = mongodb_table_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_url=crawler.settings.get('MONGODB_URL'),
            mongodb_db=crawler.settings.get('MONGODB_DB'),
            mongodb_table_name=crawler.settings.get('MONGODB_TABLE_NAME')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongodb_url)
        self.db = self.client[self.mongodb_db]

    def process_item(self, item, spider):
        self.db[self.table_name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

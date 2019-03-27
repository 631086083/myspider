# -*- coding: utf-8 -*-

import pymysql
import codecs
import json
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import pymysql.cursors
# import pymongo
from scrapy.conf import settings

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JsonWithEncodingPipeline(object):
    """
        item 转json存储
    """
    def __init__(self):
        self.file = codecs.open('article', 'w', 'utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MysqlTwistedPipeline(object):
    """
        使用twisted将mysql插入数据库，异步执行
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dict0 = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            # db="spider2",
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dict0)
        return cls(dbpool)

    def process_item(self, item, spider):
        try:
            if len(item['prop_val']) > 0:
                query = self.dbpool.runInteraction(self.do_insert, item)
                query.addErrback(self.handle_error)
        except Exception as e:
            pass

    def handle_error(self, failure):
        print(failure)
        pass

    def do_insert(self, cursor, item):
        sql = """insert into wiki_weapon(entity_name,prop_name,prop_val) VALUES (%s,%s,%s)"""
        parms = (item['entity_name'], item['prop_name'], item['prop_val'])
        cursor.execute(sql, parms)


class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect('127.0.0.1',
                                    'root', 'root', db='***', charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = """update orgcn1 set url=%s  where name=%s"""
        parms = (item['keyurl'], item['key'])
        self.cursor.execute(sql, parms)
        self.conn.commit()
        return item


class TextPipeline(object):
    def process_item(self, item, spider):
        name = item['url'].replace('/', '@').replace('?', '#')
        with open(str(name), 'w+') as f:
            f.write(item['text'])
        return item


# class MongoDbInsertPipeline(object):
#     def __init__(self):
#         host = settings["MONGODB_HOST"]
#         port = settings["MONGODB_PORT"]
#         dbname = settings["MONGODB_DBNAME"]
#         sheetname = settings["MONGODB_SHEETNAME"]
#         # 创建MONGODB数据库链接
#         client = pymongo.MongoClient(host=host, port=port)
#         # 指定数据库
#         mydb = client[dbname]
#         # 存放数据的数据库表名
#         self.post = mydb[sheetname]
#
#     def process_item(self, item, spider):
#         try:
#             data = dict(item['carsitem'])
#
#             self.post.insert(data)
#         except Exception as e:
#             print(e)
#         return item





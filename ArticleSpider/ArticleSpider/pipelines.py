# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import codecs
import json
import MySQLdb
import MySQLdb.cursors



class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    # 重载item_completed函数
    def item_completed(self, results, item, info):
        if 'front_image_url' in item:
            for ok,value in results:
                image_file_path = value['path']
            item['front_image_local_path'] = image_file_path

        return item


class JsonWithEncodingPipeline(object):
    # 自定义写入json文件方法
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding='utf-8') # 使用codecs模块保证编码与python2兼容

    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.file.write(lines)
        return item

    def spider_closed(self,spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 调用scrapy提供的JsonItemExporter写入json文件
    def __init__(self):
        self.file = open('article_exporter.json','wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.fields_to_export()
        self.file.close()

    def process_item(self,item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    # 插入数据库(同步的方式)
    def __init__(self):
        self.conn = MySQLdb.connect(host='127.0.0.1',user = 'root',passwd='123456',
                                    db='article_db',charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self,item, spider):
        insert_sql = """
            INSERT INTO jobbole_article(title, url, create_time, praise_num,url_object_id)
            VALUES(%s, %s, %s, %s,%s)
        """
        self.cursor.execute(insert_sql, (item['title'],item['url'],
                                         item['create_time'],item['praise_num'],
                                         item['url_object_id']))
        self.conn.commit()


class MysqlTwistedPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        db_params = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            cursorclass= MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb',**db_params)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item) # 将do_insert插入item这个操作变成异步
        query.addErrback(self.handler_error, item, spider) # 处理异常

    def handler_error(self, failure, item, spider):
        # 异步错误处理函数
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """
                INSERT INTO jobbole_article(
                title, 
                url, 
                create_time, 
                praise_num, 
                url_object_id,
                bookmark_num,
                comment_num,
                tag,
                front_image_url,
                front_image_local_path
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(insert_sql, (item['title'],
                                    item['url'],
                                    item['create_time'],
                                    item['praise_num'],
                                    item['url_object_id'],
                                    item['bookmark_num'],
                                    item['comment_num'],
                                    item['tag'],
                                    item['front_image_url'],
                                    item['front_image_local_path']
                                    ))

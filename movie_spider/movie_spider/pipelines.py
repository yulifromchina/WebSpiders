# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class MovieSpiderPipeline(object):
    #def process_item(self, item, spider):
        #return item
	

	def __init__(self):
		#初始化函数，新建movie_info.json文件用于存储信息
		self.file = open("movie_info.json","w",encoding="utf-8")

	
	def process_item(self, item, spider):
		if spider.name == "comedy":
			line = json.dumps(dict(item), ensure_ascii=False) + "\n"
			#json.dumps 把字典转化为字符串,ensure_ascii=True,则会忽略所有非ascii字符；ensure_ascii=False，则原样写入
			self.file.write(line)
			return item  #去掉这句则终端不会打印
		else:
			#打印全部数据
			print("name", type(item["name"]), len(item["name"]))
			print("pic", type(item["pic"]), len(item["pic"]))
			print("content", type(item["content"]), len(item["content"]))
			print("name", type(item["name"]), len(item["name"]))


	def spider_closed(self, spider):
		#爬虫关闭时处理文件
		self.file.close()

#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import scrapy
from ..items import MovieSpiderItem

class movie87_spider(scrapy.Spider):
	name = "comedy"
	allowed_domains = ["www.87movie.com"]
	start_urls = ["http://www.87movie.com/tag/%e5%96%9c%e5%89%a7"]#喜剧分类

	
	def parse_info(self, response):
		movie_info = response.meta["movie_info"]#获取传递过来的参数
		movie_info["name"] = response.xpath("//div[@class='white-div']//h3/text()").extract()
		movie_info["pic"] = response.xpath("//div[@class='white-div']//img/@src").extract()
		movie_info["content"] = response.xpath("//div[@class='white-div']//div[@class='col-md-8']/text()").extract()#先获取所有文字，再通过列表获取简介
		movie_info["content"] = movie_info["content"][-2]
		movie_info["download"] = response.xpath("//ul[@class='list-unstyled']//a/@href").extract()
		return movie_info #最外层函数，直接返回数据



	def parse_page(self, response):
		movies = response.xpath("//ul[@class='list-unstyled mlist']/li//h4/a/@href").extract()	
		url_host = "http://"+response.url.split("/")[2]
		for i in movies:
			#获取每一部电影的url
			movie_info = MovieSpiderItem()
			yield scrapy.Request(url_host+i, meta={"movie_info":movie_info}, callback = self.parse_info)#把每一部电影的链接传递给回调函数，参数通过meta字典来传递


	def parse(self, response):
	#获取电影每一页的url
		num_page = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").extract()
		number = 1
		if len(num_page)>0:#大于0页
			number = int(num_page[0].split("/")[-1].split("?")[0])
		#number=1#for debug
		for i in range(1,number+1):
			yield scrapy.Request(response.url+"/"+str(i)+"?o=data", callback=self.parse_page)#将每一页的链接丢到回调函数parse_page中
	

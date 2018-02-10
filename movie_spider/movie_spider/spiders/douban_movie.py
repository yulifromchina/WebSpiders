#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import scrapy
from ..items import MovieSpiderItem

class db_movie(scrapy.Spider):
	name = "douban_movie"
	allowed_domains = ["movie.douban.com"]
	start_urls = ["https://movie.douban.com/cinema/later/beijing/"]


	def parse_info(self, response):
		movie_info = MovieSpiderItem()
		movie_info["name"] = response.xpath("//div[@id='content']/h1/span/text()").extract()
		movie_info["pic"] = response.xpath("//div[@id='mainpic']/a/img/@src").extract()
		movie_info["content"] = response.xpath("//div[@id='link-report']/span/text()").extract()
		movie_info["download"] = ""
		print(movie_info)

	
	def parse(self,response):
		movie_links = response.xpath("//div[@id='showing-soon']/div/a/@href").extract()
		for i in movie_links:
			#将每一个电影链接传递给回调函数处理
			yield scrapy.Request(i, callback=self.parse_info)

#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import requests
import logging
import logging.config
import time
from bs4 import BeautifulSoup
from database import *

logging.config.fileConfig("logger.conf")
logger = logging.getLogger("spiderLogger")


def write_database(movie_title, score, judge_people,info, url):
	insert_or_update_data(movie_title, float(score),int(judge_people), info, url)


def get_movie_link(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	movies = soup.find_all("div",{"class":"item"})
	for i in movies:
		href = i.find("div",{"class":"pic"}).find("a").get("href")
		title = i.find("span",{"class":"title"}).get_text()
		score = i.find("span",{"class":"rating_num"}).get_text()
		judge_people = i.find("div",{"class":"star"}).find_all("span")[-1].get_text()
		judge_people = re.sub("\D","",judge_people)
		try:
			info = i.find("span",{"class":"inq"}).get.text()
		except:
			info = "无介绍"
		logger.debug("href:{} title:{} score:{} judge_people:{} info:{}".format(href, title, score, judge_people, info))
		write_database(movie_title=title, score=score, judge_people=judge_people,info=info,url=href)
		time.sleep(0.5)
		

		
def main():
	res = requests.get("https://movie.douban.com/top250")
	soup = BeautifulSoup(res.text, 'lxml')
	page_link = "https://movie.douban.com/top250?start={}&filter="
	page = soup.find_all("div",{"class":"paginator"})
	if len(page)>1:
		return
	a_content = page[0].find_all("a",recursive = False)
	page_list = [1]
	for i in a_content:
		page_start = int(i.get("href").split("=")[1].split("&")[0])
		page_list.append(page_start)
	for i in page_list:
		logger.debug(page_link.format(i))
		get_movie_link(page_link.format(i))


if __name__ == "__main__":
	main()

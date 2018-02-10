#!/usr/bin/env python3


import logging
import logging.config
logging.config.fileConfig("logger.conf")
logger = logging.getLogger("dbLogger")
import sqlite3

base_url = "./movie.db"
table_name = "movie_table"

def create_table():
	sql3_db = sqlite3.connect(base_url)
	create_sql = "CREATE TABLE {} (movie_title varchar(1024), score decimal(8,8), judge_people int, info varchar(1024), url varchar(1024))".format(table_name)
	try:
		sql3_db.execute(create_sql)
	except:
		logging.debug("create table fail, for table exits")
		return False

	sql3_db.close()
	logging.debug("create table success")
	return True


def query(title):
	sql3_db = sqlite3.connect(base_url)
	query_sql = "select * from {} where movie_title = {}".format(table_name, title)
	cur = sql3_db.cursor()#在存储结果中遍历所得的结果集时，使用游标
	try:
		cur.execute(query_sql)
	except:
		logging.error("query fail, sql :{}".format(query_sql))
		sql3_db.close()
		return False
	record_list = cur.fetchall()
	if len(record_list)>0:
		logging.debug("query success")
		return True
	return False




def insert_or_update_data(movie_title, score, judge_people, info, url):
	create_table()
	if query(movie_title):#查询得到movie_title，说明数据存在，只需更新
		sql3_db = sqlite3.connect(base_url)
		update_sql = "update {} set score={}, judge_people={},info='{}',url='{}' where movie_title='{}'".format(table_name,score, judge_people, info, url, movie_title)
		try: 
			sql3_db.execute(update_sql)
			sql3_db.commit()#执行更新操作，数据的提交，需要执行commit函数
		except:
			logging.error("update fail, sql:{}".format(update_sql))
			return False
		sql3_db.close()
	else:#查询不到movie_title，说明数据不存在，执行插入操作
		sql3_db = sqlite3.connect(base_url)
		insert_sql = "INSERT INTO {} (movie_title, score, judge_people, info, url) values ('{}',{},{},'{}','{}')".format(table_name,movie_title, score, judge_people, info, url)
		try:
			sql3_db.execute(insert_sql)
			sql3_db.commit()
		except:
			logging.error("insert fail, sql:{}".format(insert_sql))
			return False
		sql3_db.close()
	logging.debug("insert or update success")
	return True
		
if __name__ == "__main__":
	movie_title = "test title"	
	score = 100.1
	judge_people = 888
	info = "test info"
	url = "test url"
	if insert_or_update_data(movie_title, score, judge_people, info, url):
		print("test success")	
	else:
		print ("test fail")

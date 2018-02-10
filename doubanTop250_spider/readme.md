### 爬虫：爬取豆瓣电影排行250

起始url:https://movie.douban.com/top250



### 文件结构：

——database.py:实现对sqlite的增、改、查

——parse.py:爬虫文件，实现从起始url爬取top250的电影信息，共10页

——logger.conf:实现日志记录，使用两个logger分别记录database和parse的日志

——movie.db:运行后生成的数据库文件

——mySpider.log:运行后生成的日志



### 涉及模块：

logging/sqlite3/re/requests/beautifulSoup/time
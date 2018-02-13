# 爬虫基础系列：

doubanTop250_spider：使用logging/sqlite3/re/requests/beautifulSoup/time完成爬取豆瓣电影250

movie_spider:使用scrapy框架完成87movie电影网喜剧类硬盘的爬取；以及豆瓣电影北京影讯的爬取

# 爬虫进阶系列：

### ArticleSpider

功能：完成伯乐在线 最新文章 的爬取，提取每篇文章的关键信息（标题，发布时间，tag，点赞数，收藏数，评论数，url, 封面图片），并保存在Mysql数据库中。

1.jobbole_spider.py的parse函数负责提取下一页的url交给回调函数parse，提取每篇文章的url交给回调函数parse_detail

2.通过items.py定义字段，把非结构化的数据保存成结构化的数据

3.通过pipelines.py中定义ArticleImagePipeLine负责下载图片

4.通过pipelines.py中定义MySQLTwistedPipeline将数据通过twisted提供线程池异步保存到本地MYSQL数据库中。




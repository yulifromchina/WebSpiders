### ArticleSpider

功能：完成伯乐在线 最新文章 的爬取，提取每篇文章的关键信息（标题，发布时间，tag，点赞数，收藏数，评论数，url, 封面图片），并保存在Mysql数据库中。

1.jobbole_spider.py：

定义parse函数负责提取下一页的url交给回调函数parse，提取每篇文章的url交给回调函数parse_detail；

使用itemloader从页面提取文章信息

2.items.py:

定义Field字段，把非结构化的数据保存成结构化的数据

3.pipelines.py:

定义ArticleImagePipeLine负责下载图片

定义JsonWithEncodingPipeline负责保存数据到Json文件

定义MySQLTwistedPipeline将数据通过twisted提供线程池异步保存到本地MYSQL数据库中。




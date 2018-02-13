# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem,ArticleItemLoader
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1.获取页面中的所有文章Url并交给scrapy下载
        2.获取下一页的url
        """

        #post_urls = response.css('#archive .floated-thumb .post-thumb a::attr(href)').extract()
        post_node = response.css('#archive .floated-thumb .post-thumb a')
        for url in post_node:
            # yield Request(url, callback=self.parse_detail)

            # parse.urljoin:Join a base URL and a possibly relative URL to form an absolute url
            # yield Request(parse.urljoin(response.url, url),callback=self.parse_detail)

            # 获取文章列表的同时，获取封面图片：通过meta传递(meta是字典类型)
            post_url = url.css('::attr(href)').extract_first('')
            image_url = url.css('img::attr(src)').extract_first('')
            yield Request(parse.urljoin(response.url, post_url), callback=self.parse_detail,
                          meta={'front_image_url':parse.urljoin(response.url,image_url)})

        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url != None:
            yield Request(parse.urljoin(response.url,next_url), callback=self.parse)



    def parse_detail(self, response):
        """
        提取文章具体字段
        """


        # 通过xpath方式提取关键值
        """
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]

        create_time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0]
        create_time = create_time.replace('·','').strip()

        praise_num = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0]
        if praise_num != '':
            praise_num = int(praise_num)
        else:
            praise_num = 0

        bookmark_num = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        bookmark_num = re.match('.*(\d+).*',bookmark_num)
        if bookmark_num:
            bookmark_num = int(bookmark_num.group(1))
        else:
            bookmark_num = 0

        comment_num = response.xpath('//span[contains(@class,"btn-bluet-bigger")][2]/text()').extract()[0]
        comment_num = re.match('.*(\d+).*',comment_num)
        if comment_num:
            comment_num = int(comment_num.group(1))
        else:
            comment_num = 0

        content = response.xpath('//div[@class="entry"]').extract()[0]

        tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tag_list = [element.strip() for element in tag_list if not  element.strip().endswith(' 评论')]
        tag = ','.join(tag_list)
        """

        # 通过css selector提取关键值

        """
        title = response.css('.entry-header h1::text').extract_first()
        # extract()[0]可能会抛异常，所以使用extract_first()

        create_time = response.css('.entry-meta-hide-on-mobile::text').extract_first().strip()
        create_time = create_time.replace('·', '').strip()

        praise_num = response.css('.vote-post-up h10::text').extract_first()
        if praise_num != '':
            praise_num = int(praise_num)
        else:
            praise_num = 0

        bookmark_num = response.css('.bookmark-btn::text').extract_first()
        bookmark_num = re.match('.*(\d+).*',bookmark_num)
        if bookmark_num:
            bookmark_num = int(bookmark_num.group(1))
        else:
            bookmark_num = 0

        comment_num = response.css('a[href="#article-comment"] span::text').extract_first()
        comment_num = re.match('.*(\d+).*', comment_num)
        if comment_num:
            comment_num = int(comment_num.group(1))
        else:
            comment_num = 0

        content = response.css('.entry').extract_first()

        tag_list = response.css('.entry-meta a::text').extract()
        tag_list = [element.strip() for element in tag_list if not  element.strip().endswith(' 评论')]
        tag = ','.join(tag_list)

        front_image_url = response.meta.get('front_image_url','')

        article_item = JobBoleArticleItem()
        article_item['url'] = response.url
        article_item['url_object_id'] = get_md5(response.url)
        article_item['title'] = title

        # 将日期保存成datetime格式
        try:
            create_time = datetime.datetime.strptime(create_time,"%Y/%m/%d").date()
        except Exception as e:
            create_time = datetime.datetime.now()

        article_item['create_time'] = create_time
        article_item['praise_num'] = praise_num
        article_item['bookmark_num'] = bookmark_num
        article_item['comment_num'] = comment_num
        article_item['content'] = content
        article_item['tag'] = tag
        article_item['front_image_url'] = [front_image_url]
        """

        # 通过ItemLoader加载item,简化代码,增加可配置性（比如把规则写到数据库中）
        #item_loader = ItemLoader(item=JobBoleArticleItem(), response=response)
        # item_loader 解析规则，生成item对象，每一个选项都会以list的方式保存
        # 使用自定义的ArticleItemLoader，便于让每个list选择第一个选项
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css('title','.entry-header h1::text')
        item_loader.add_css('create_time','.entry-meta-hide-on-mobile::text')
        item_loader.add_css('praise_num','.vote-post-up h10::text')
        item_loader.add_css('bookmark_num','.bookmark-btn::text')
        item_loader.add_css('comment_num','a[href="#article-comment"] span::text')
        item_loader.add_css('tag','.entry-meta a::text')
        item_loader.add_value('front_image_url',response.meta.get('front_image_url',''))
        item_loader.add_value('url',response.url)
        item_loader.add_value('url_object_id',get_md5(response.url))

        article_item = item_loader.load_item()


        yield article_item  # 路由到pipelines进行处理

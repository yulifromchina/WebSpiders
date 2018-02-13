# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def data_convert(value):
    # 将日期保存成datetime格式
    try:
        create_time = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_time = datetime.datetime.now().date()
    return create_time


def get_nums(value):
    value = re.match('.*(\d+).*', value)
    if value:
        value = int(value.group(1))
    else:
        value = 0
    return value


def remove_comment_tags(value):
    if '评论' in value:
        return ''
    else:
        return value


def return_value(value):
    # trick
    return value


class ArticleItemLoader(ItemLoader):
    # 重载类，解决默认ItemLoader取整个列表的问题
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_time = scrapy.Field(
        input_processor = MapCompose(data_convert)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()  # url可能比较长，该字段存放url的md5
    praise_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    bookmark_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content = scrapy.Field()
    tag = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor = Join(',')
    )
    front_image_url = scrapy.Field(
        output_processor= MapCompose(return_value) # 覆盖默认的TakeFirst()
    )
    front_image_local_path = scrapy.Field()  # 如果把封面图片存放在本地时的路径

    pass

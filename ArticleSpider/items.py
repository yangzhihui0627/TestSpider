# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Compose
import re
import datetime


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItemLoader(ItemLoader):
    #由于itemloader根据选择器取到的值为list，因此自定义item_loader并修改默认取fist值
    default_output_processor = TakeFirst()


def RepleaseStrip(date):
    #日期去除空格及点
    create_data =  date[0].strip().replace("·","").strip()
    try:
        create_data = datetime.datetime.strftime(create_data, "%Y/%m/%d").date()
    except Exception as er:
        create_data = datetime.datetime.now().date()
    return create_data


def ReNumber(value):
    #将字符数字转化为int类型
    match_re = re.match(".*?(\d+).*", value[0])
    nums = 0
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums

class JobbboleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        #调用自定义函数RepleaseStrip处理itemloader取出来的日期
        input_processor = Compose(RepleaseStrip)
    )
    praise_nums = scrapy.Field(
        output_processor=Compose(ReNumber)
    )
    book_mark = scrapy.Field(
        #尽量将ReNumber处理函数绑定在output_processor上，避免函数处理过程中结果为0 时
        # itemloader取TakeFirst()由于为空会丢弃该字段，导致itemloader丢失该字段而无法将所有字段正确赋值给item字段，插入
        # 数据库时因找不到字段而报错
        output_processor=Compose(ReNumber)
    )
    comment_nums = scrapy.Field(
        output_processor=Compose(ReNumber)
    )
    content = scrapy.Field()
    url = scrapy.Field()
#item中调用的Compose函数，用于处理item中的值，这里处理了字符串替换
def Replace(content):
    new_content = content.replace('2312','k')
    return new_content
#抓取python学习静态页面
class PythonDoc(scrapy.Item):
    content = scrapy.Field()
    file_name = scrapy.Field(
        output_processor = Compose(Replace)
    )
#喜马拉雅MP3资源下载
class XimalayaMp3(scrapy.Item):
    nickName = scrapy.Field()
    title = scrapy.Field()
    playUrl = scrapy.Field()
    save_path = scrapy.Field()
    createdAt = scrapy.Field()
    playTimes = scrapy.Field()
    smallLogo = scrapy.Field()
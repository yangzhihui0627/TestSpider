# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import PythonDoc
import datetime

class PythonDocSpider(scrapy.Spider):
    name = 'pythonDoc'
    allowed_domains = ['www.kuqin.com']
    start_urls = ['http://www.kuqin.com/abyteofpython_cn/index.html']

    """
    获取列表页post_urls
    并将每页Request发送scrapy下载器处理
    :param response:
    :return:
    """
    def parse(self, response):
        post_urls = response.css("a::attr(href)").extract()
        for post_url in post_urls:
            yield Request(url = parse.urljoin(response.url,post_url),callback = self.parse_detail)

        next_urls = response.css("[align=right]>a::attr(href)").extract()[0]
        if next_urls:
            yield Request(url = parse.urljoin(response.url,next_urls),callback = self.parse)

    def parse_detail(self, response):
        doc_item = PythonDoc()
        content = response.text
        doc_item['content'] = content.replace("2312","k")
        doc_item['file_name'] = response.url
        yield doc_item
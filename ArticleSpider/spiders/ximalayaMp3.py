# encoding = utf-8
__author__ = 'young'
import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import XimalayaMp3
pageId = 1
header = {
        "HOST": "mobwsa.ximalaya.com",
        "Referer": "http://mobwsa.ximalaya.com/mobile/v1/album/ts-1513773880509?ac=WIFI&albumId=9742789&device=android&isAsc=true&pageId=1&pageSize=20&pre_page=0&supportWebp=true",
        "User-Agent": "ting_6.3.60(MI+5,Android24)"
    }
class XimalayaMp3Spider(scrapy.Spider):
    name = 'ximalayaMp3'
    allowed_domains = ['mobwsa.ximalaya.com']
    start_urls = ['http://mobwsa.ximalaya.com/mobile/v1/album/track/ts-1514281193467?'
                    'albumId=9742789&device=android&isAsc=true&pageId=1&pageSize=20&pre_page=0']

    def parse(self, response):
        ++pageId
        next_urls = '''http://mobwsa.ximalaya.com/mobile/v1/album/track/ts-1514281193467?albumId=9742789&device=android&isAsc=true&pageId=%s&pageSize=20&pre_page=0''' %(pageId)
        if pageId == 20:
            yield Request(url=parse.urljoin("http://mobwsa.ximalaya.com", next_urls), callback=self.parse,headers=header)

    def parse_detail(self, response):
        doc_item = XimalayaMp3()
        content = response.text
        doc_item['content'] = content.replace("2312","k")
        doc_item['file_name'] = response.url
        yield doc_item
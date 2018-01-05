# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobbboleItem,ArticleItemLoader
import datetime
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        获取列表页post_urls
        并将每页请求发送scrapy下载器处理
        :param response:
        :return:
        """
        post_urls = response.css("#archive .floated-thumb .align-right a::attr(href)").extract()
        for post_url in post_urls:
            yield Request(url = parse.urljoin(response.url,post_url),callback = self.parse_detail)

        next_urls = response.css(".next.page-numbers::attr(href)").extract()[0]
        if next_urls:
            yield Request(url = parse.urljoin(response.url,next_urls),callback = self.parse)

    def parse_detail(self,response):
        article_item =  JobbboleItem()
        if( response.url== 'http://blog.jobbole.com/all-posts/'):
            pass
        # url = response.url
        # title = response.xpath('//*[@class="entry-header"]/h1/text()').extract()[0]
        # create_date = response.xpath('//*[@class="entry-meta"]/p/text()').extract()[0].strip().replace("·","").strip()
        # praise_nums = int(response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0])
        # book_mark = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # match_re = re.match(r".*(\d+).*",book_mark)
        # match_com = re.match(r".*(\d).*",comment_nums)
        # content = response.xpath("//*[@class='entry']/p/text()").extract()[0]
        # if match_re:
        #     book_mark = int(match_re.group(1))
        # else:
        #     book_mark = 0
        # if match_com:
        #     comment_nums = int(match_com.group(1))
        # else:
        #     comment_nums = 0
        # article_item['title'] = title
        # """
        # 将字符串日期格式化为date类型
        # """
        # try:
        #     create_date = datetime.datetime.strftime(create_date,"%Y/%m/%d").date()
        # except Exception as er:
        #     create_date = datetime.datetime.now().date()
        # article_item['create_date'] = create_date
        # article_item['praise_nums'] = praise_nums
        # article_item['book_mark'] = book_mark
        # article_item['comment_nums'] = comment_nums
        # article_item['content'] = content
        # article_item['url'] = url

        #通过itemLoader加载 item
        item_loader = ArticleItemLoader(item=JobbboleItem(),response=response)
        item_loader.add_xpath("title",'//*[@class="entry-header"]/h1/text()')
        item_loader.add_value("url",response.url)
        item_loader.add_xpath("create_date",'//*[@class="entry-meta"]/p/text()')
        item_loader.add_xpath("praise_nums","//span[contains(@class,'vote-post-up')]/h10/text()")
        item_loader.add_xpath("book_mark","//span[contains(@class,'bookmark-btn')]/text()")
        item_loader.add_xpath("comment_nums","//a[@href='#article-comment']/span/text()")
        item_loader.add_xpath("content","//*[@class='entry']/p/text()")
        article_item = item_loader.load_item()
        yield article_item

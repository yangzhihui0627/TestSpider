# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from scrapy.http import Request
import urllib
"""
twisted.enterprise 异步操作数据库adbapi
"""
from twisted.enterprise import adbapi

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item
"""
simple insert sql
"""
class MysqlPipeLine(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host = "localhost",user = "root",password = "",database = "test",port = 3306,charset="utf8",use_unicode = True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
        insert into article_jobbole(url,title,create_date,book_mark,content,praise_nums,comment_nums) VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item['url'],item['title'],item['create_date'],item['book_mark'],item['content'],
                                        item['praise_nums'],item['comment_nums']))
        self.conn.commit()

"""
ansy insert sql by twisted
"""
class MysqlTwistedPipline(object):
    #初始化数据库链接池
    def __init__(self, dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            user = settings['MYSQL_USER'],
            password = settings['MYSQL_PASSWORD'],
            db = settings['MYSQL_DBNAME'],
            port = settings['MYSQL_POET'],
            charset = "utf8",
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparams)
        return cls(dbpool)
    def process_item(self,item,spider):
        #使用twisted将sql异步插入数据库
        query = self.dbpool.runInteraction(self.doInsert,item)
        query.addErrback(self.handler_error,item,spider)
    def handler_error(self,failuer,item,spider):
        #处理异步插入的异常
        print(failuer)
    def doInsert(self,cursor,item):
        #执行具体插入
        insert_sql = """
                insert into article_jobbole(url,title,create_date,book_mark,content,praise_nums,comment_nums) VALUES (%s,%s,%s,%s,%s,%s,%s)
                """
        cursor.execute(insert_sql,
                        (item['url'], item['title'], item['create_date'], item['book_mark'], item['content'],
                         item['praise_nums'], item['comment_nums']))


"""
 保存pythonDoc静态页面
"""
class StorePythonDoc(object):
    def process_item(self,item,spider):
        content = item['content']
        # file_name = item['file_name']
        file_name = item['file_name']
        name = file_name.rsplit('/',1)
        self.save_to_file(name[1],content)

    def save_to_file(self,file_name,content):
        fn = open(file_name,mode="w",encoding='GBK')
        fn.write(content)
        fn.close()

"""
 爬取喜马拉雅相声
"""
# class StoreMp3Xmla(object):
#     arryList = [{1,'http://audio.xmcdn.com/group31/M04/35/C1/wKgJSVmC5lfDDD60AKZuRGS9gEU329.mp3'}
#                 ,{2,'http://audio.xmcdn.com/group30/M06/D5/13/wKgJXlmG0vSC4NTvAUj9xxnKzpQ435.mp3'}
#                 ,{3,'http://audio.xmcdn.com/group30/M06/D5/1A/wKgJXlmG0wOjdbIxAOe8osMsrMQ770.mp3'}
#                 ,{4,'http://audio.xmcdn.com/group30/M06/D5/1A/wKgJXlmG0wSQrRbAAM2M9mEpFwQ950.mp3'}
#                 ,{5,'http://audio.xmcdn.com/group30/M00/67/19/wKgJXlmC5izzLctkAM0ewiXxQPc130.mp3'}]
#     for index,item in arryList:
#         print(item)
#         req = urllib.request.Request(item)
#         response = urllib.request.urlopen(req)
#         con = response.read()
#         with open("d:/"+str(index)+".mp3", "wb") as code:
#             code.write(con)
#     pass

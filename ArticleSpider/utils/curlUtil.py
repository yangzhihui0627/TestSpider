# -*- coding: utf-8 -*-

import pycurl
import urllib
import os
import time

def initCurl():
    '''初始化一个pycurl对象，
    尽管urllib2也支持 cookie 但是在登录cas系统时总是失败，并且没有搞清楚失败的原因。
    这里采用pycurl主要是因为pycurl设置了cookie后，可以正常登录Cas系统
    '''
    c = pycurl.Curl()
    # c.setopt(pycurl.COOKIEFILE, "cookie_file_name")  # 把cookie保存在该文件中
    # c.setopt(pycurl.COOKIEJAR, "cookie_file_name")
    # c.setopt(pycurl.FOLLOWLOCATION, 1)  # 允许跟踪来源
    # c.setopt(pycurl.MAXREDIRS, 5)
    # 设置代理 如果有需要请去掉注释，并设置合适的参数'
    # c.setopt(pycurl.PROXY, ‘http://11.11.11.11:8080′)
    c.setopt(pycurl.PROXYUSERPWD, 'testuser:123123')
    return c


def GetDate(curl, url):
    '''获得url指定的资源，这里采用了HTTP的GET方法
'''
    head = ['Accept:*/*'
        ,
            'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
            ]
    # buf = StringIO.StringIO()
    # curl.setopt(pycurl.WRITEFUNCTION, buf.write)
    # curl.setopt(pycurl.URL, url)
    # curl.setopt(pycurl.HTTPHEADER, head)
    # curl.perform()
    # the_page = buf.getvalue()
    # buf.close()
    # return the_page


def PostData(curl, url, data):
    '''提交数据到url，这里使用了HTTP的POST方法
    备注，这里提交的数据为json数据，
    如果需要修改数据类型，请修改head中的数据类型声明
    '''
    head = ['Accept:*/*'
        , 'Content-Type:application/xml'
        , 'render:json'
        , 'clientType:json'
        , 'Accept-Charset:GBK,utf-8;q=0.7,*;q=0.3'
        , 'Accept-Encoding:gzip,deflate,sdch'
        , 'Accept-Language:zh-CN,zh;q=0.8'
        ,
            'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
            ]
    # buf = StringIO.StringIO()
    # curl.setopt(pycurl.WRITEFUNCTION, buf.write)
    # curl.setopt(pycurl.POSTFIELDS, data)
    # curl.setopt(pycurl.URL, url)
    # curl.setopt(pycurl.HTTPHEADER, head)
    # curl.perform()
    # the_page = buf.getvalue()
    # print the_page
    # buf.close()
    # return the_page
    c = pycurl.Curl()
    c.setopt(pycurl.PROXYUSERPWD, 'testuser:123123')
    c.setopt(c.URL, 'http://fileserver.ptengine.cn/page/test/bg-btn-blue.png')
    c.setopt(c.HTTPPOST, [
        ('fileupload', (
            # upload the contents of this file
            c.FORM_FILE, '/data/history_heat_maps/page/test/bg-btn-blue.png',
            # specify a different file name for the upload
            # c.FORM_FILENAME,'/data/history_heat_maps/page/'+ 'helloworld.py',
            # specify a different content type
            # c.FORM_CONTENTTYPE, 'application/x-python',
        ))
    ])

    c.perform()
    c.close()

"""
   python获取目录文件列表
"""
def getFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            #如果需要忽略某些文件夹，使用以下代码
            #if s == "xxx":
                #continue
            newDir=os.path.join(dir,s)
            getFileList(newDir, fileList)
    return fileList

"""
 生成多行curl上传文件命令
 curl --user testuser:123123 -T /data/history_heat_maps/page/test/bg-btn-blue.png http://fileserver.ptengine.cn/page/test/bg-btn-blue.png
curl --user testuser:123123 -T /data/history_heat_maps/page/test/bg-next-green.png http://fileserver.ptengine.cn/page/test/bg-next-green.png
curl --user testuser:123123 -T /data/history_heat_maps/page/test/bg-prev-green.png http://fileserver.ptengine.cn/page/test/bg-prev-green.png
"""
def upload_exe(dir, fileList):
    newDir = dir
    os_head = 'curl --user testuser:123123 -T '
    os_fileserver = ' http://fileserver.ptengine.cn/resource/'
    if os.path.isfile(dir):
        fileserver = dir.replace("/data/history_heat_maps/resource/",os_fileserver)
        fileList.append(os_head+dir+fileserver)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            #如果需要忽略某些文件夹，使用以下代码
            #if s == "xxx":
                #continue
            newDir=os.path.join(dir,s)
            upload_exe(newDir, fileList)
    return fileList

if __name__ == '__main__':
    # os.path.dirname(os.path.abspath('1508656591862.html'))
    # '/data/history_heat_maps/page/fea86ab18a02314dac290a2e45e0442c'
    print(os.path.dirname(os.path.abspath("curlUtil.py")))
    # 生成批量上传文件命令
    list = upload_exe(os.path.dirname(os.path.abspath("curlUtil.py")), [])
    for e in list:
        print(e)
        # 批量上传文件时开启下列命令
        os.system(e)
        time.sleep(2)
    pass



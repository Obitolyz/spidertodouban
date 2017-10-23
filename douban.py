#!/usr/bin/env python
#coding:utf-8

import requests
import re
from bs4 import BeautifulSoup
from Queue import Queue
import os
import json
from time import sleep
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# import pymysql
# import pymysql.cursors
# config = {
#     'host':'127.0.0.1',
#     'port':3306,
#     'user':'root',
#     'passwd':'654321',
#     'db':'douban_database',
#     'use_unicode':1,
#     'charset':'utf8',
#     'cursorclass':pymysql.cursors.DictCursor          # 以字典形式返回,默认是元组
# }
# connection = pymysql.Connect(**config)

HEADER={
"Host": "movie.douban.com",
"scheme":"https",
"version":"HTTP/1.1",
"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q = 0.8",
"accept-encoding":"gzip,deflate,sdch",
"accept-language":"zh-CN,zh;q=0.8",
"cache-control":"max-age=0",
"cookie":'',                           # add your cookie
"referer":"https://book.douban.com/subject/26757148/?icn=index-editionrecommend",
"upgrade-insecure -requests":"1",
"user-agent":"Mozilla / 5.0(WindowsNT6.3;"   \
	"WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 48.0.2564.116Safari / 537.36"
}

class DouBanMovieSpider(object):

    def __init__(self,connection):
        self.url = 'https://movie.douban.com/'
        self.myQueue = Queue(maxsize = -1)
        self.visited = set()
        self.num = 1
        self.dirname = 'D:/PycharmProjects/data/'
        self.connection = connection

    def get_movie_infor(self,html,url):
        soup = BeautifulSoup(html,'html.parser')
        # 电影名字
        try:
            movie_name = soup.find('span',attrs = {'property':"v:itemreviewed"}).string
        except Exception:
            movie_name = ''
        # 导演
        try:
            movie_diretor = soup.find('a',attrs = {'rel':'v:directedBy'}).string
        except Exception:
            movie_diretor = ''
        # 主演
        try:
            movie_star = []
            ls = soup.find_all('a',attrs = {'rel':'v:starring'})
            for x in ls:
                movie_star.append(x.string)
            movie_star_ss = ','.join(movie_star)
        except Exception:
            movie_star = []
            movie_star_ss = ''
        # 评分
        try:
            movie_score = soup.find('strong',attrs = {'property':"v:average"}).string
        except Exception:
            movie_score = ''
        # 时长
        try:
            movie_runtime = soup.find('span',attrs = {'property':'v:runtime'}).get('content')
        except Exception:
            movie_runtime = ''
        # 上映时间
        try:
            movie_date = soup.find('span',attrs = {'property':'v:initialReleaseDate'}).string
        except Exception:
            movie_date = ''
        # 地区
        try:
            pattern = u'<span\s+class=["\']pl["\']>制片国家/地区:</span>(.*?)<br/>'    # 匹配中文的话要加个u
            movie_area = re.findall(pattern,html)[0].lstrip()    # 去掉左边多余的空格   strip lstrip rstrip replace
        except Exception:
            movie_area = ''
        # 类型
        movie_type = []
        try:
            ls = soup.find_all('span',attrs = {'property':'v:genre'})
            for x in ls:
                movie_type.append(x.string)
            movie_type_ss = ','.join(movie_type)              # 还原: movie_type_ss.split(',')  拆分字符串为列表
        except Exception:
            movie_type = []
            movie_type_ss = ''
        # 电影基本信息
        # info = {
        #     'name':movie_name,
        #     'diretor':movie_diretor,
        #     'star': movie_star,     # 也是个列表
        #     'score':movie_score,
        #     'runtime':movie_runtime,
        #     'date':movie_date,
        #     'area':movie_area,
        #     'type':movie_type,      # 是个列表
        #     'url':url
        # }
        info = (
            movie_name,
            movie_diretor,
            movie_star_ss,
            movie_score,
            movie_runtime,
            movie_date,
            movie_area,
            movie_type_ss,
            url
        )
        return info

    def write_infor_to_file(self,html,infor,n):
        # filename = os.path.join(self.dirname,'{}.txt'.format(n))
        # fp = open(filename,'w')
        # json.dump(infor,fp,ensure_ascii=False)
        # fp.close()
        try:
            with self.connection.cursor() as cursor:
                # sql = 'CREATE DATABASE douban_database'   # 创建数据库
                # cursor.execute(sql)

                # sql = 'USE douban_database'               # 使用数据库
                # cursor.execute(sql)

                sql = 'create table if not exists douban(name varchar(1000),diretor varchar(1000),star varchar(1000),' \
                      'score varchar(1000),runtime varchar(1000),' \
                      'date varchar(1000),area varchar(1000),type varchar(1000),url varchar(1000))'  # 创建表
                cursor.execute(sql)

                sql = "replace into douban(name,diretor,star,score,runtime,date,area,type,url) " \
                      "values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                cursor.execute(sql % infor)
                self.connection.commit()

                # print '插入',cursor.rowcount,'条数据'
        except Exception:
            pass
        finally:
            # self.connection.close()
            pass
    def spider_to_spider(self):
        record = {}
        while not self.myQueue.empty():
            url = self.myQueue.get()
            try:
                if url not in self.visited:
                    sleep(1)                        # 延时一秒,防止被发现
                    response = requests.get(url, headers = HEADER)
                else:
                    continue
            except Exception:
                pass
            else:
                if response.status_code == 200:    # 访问成功
                    response.encoding = 'utf-8'
                    html = response.text           # 得到网页
                    if re.findall(u'单集片长',html):
                        continue
                    next_movie_urls = self.get_movie_url(html)      # 相似的电影入队
                    for ul in next_movie_urls:
                        self.myQueue.put(ul)
                    infor = self.get_movie_infor(html,url)       # 获取电影数据
                    self.write_infor_to_file(html,infor,self.num)     # 将数据写入文档
                    self.num += 1
                    self.visited.add(url)
                else:                            # 访问失败,重新添加,直到3次
                    print '访问失败...'
                    times = record.get(url,0)
                    if times == 3:
                        continue
                    record[url] = times + 1
                    self.myQueue.put(url)

    def get_movie_url(self, html):
        pattern = 'https://movie.douban.com/subject/\d{8}/\?from'  # 匹配模式
        soup = BeautifulSoup(html,'html.parser')
        movie_list = soup.find_all('a',attrs={'href':re.compile(pattern)})   # or href = re.compile(pattern)
        urls = [movie.get('href') for movie in movie_list]

        num = len(movie_list)
        for n in range(0,num):            # 去掉后缀，避免重复
            urls[n] = urls[n][0:41]

        return urls

    def spider(self):

        response = requests.get(self.url, headers = HEADER)  # 打开主页
        if response.status_code != 200:
            print 'fail to open the main webpage...'
        response.encoding = 'utf-8'
        html = response.text
        movie_urls = self.get_movie_url(html)    # 得到电影链接
        simple = []
        for url in movie_urls:
            if url not in simple:
                # print url
                self.myQueue.put(url)               # 入队
                simple.append(url)
        simple = []
        self.spider_to_spider()



# if __name__ == '__main__':
#     doubansp = DouBanMovieSpider(connection)
#     doubansp.spider()
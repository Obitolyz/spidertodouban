#!/usr/bin env python
#coding=utf-8

import pymysql
import pymysql.cursors
from time import sleep
from langconv import *
import json

import sys
reload(sys)
sys.setdefaultencoding('utf8')        # 这个就很厉害了，设置默认编码

config = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'passwd':'654321',
    'db':'douban_database',     # 选择数据库
    'use_unicode':1,
    'charset':'utf8',
    'cursorclass':pymysql.cursors.DictCursor             # 以字典形式返回,默认是元组
}

connection = pymysql.Connect(**config)

# if __name__ == '__main__':
#     try:
#         with connection.cursor() as cursor:
#             sql = 'create table if not exists watched(name varchar(1000),diretor varchar(1000),star varchar(1000),' \
#                   'score varchar(1000),runtime varchar(1000),' \
#                   'date varchar(1000),area varchar(1000),type varchar(1000),url varchar(1000))'  # 创建表
#             cursor.execute(sql)
#             sql = 'select * from douban'
#             cursor.execute(sql)
#             infors = cursor.fetchall()
#             fp = open('D:/PycharmProjects/_datasheets/test_zone.txt','r')
#             ListForArea = json.load(fp)
#             fp.close()
#             for Area in ListForArea:
#                 # print Area
#                 for ss in infors:
#                     sarea = ss['area'].replace(' ','').split('/')   # 去掉多余的空格然后切分开来(ps:存数据的时候忘记处理空格了)
#                     for el in sarea:
#                         newel = filter(lambda c : u'\u4e00' <= c <= u'\u9fa5',el)   # 去掉非中文字母(这里是为了去掉英文字母)
#                         # print newel
#                         # 将繁体字转化为简体字   other(Converter('zh-hant').convert(newel)
#                         newel = Converter('zh-hans').convert(newel)
#                         if newel == Area:
#                             sql = "replace into zone(zone_name,name,diretor,star,score,runtime,date,area,type,url) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
#                             cursor.execute(sql % (Area,ss['name'],ss['diretor'],ss['star'],ss['score'],ss['runtime'],ss['date'],ss['area'],ss['type'],ss['url']))
#                 print 'insert...'
#             print 'ok...'
#
    #         connection.commit()            # 提交数据
    #         cursor.close()                 # 关闭游标
    # finally:
    #     connection.close()             # 关闭连接

#!/usr/bin/env python
# -*- coding:utf-8 -*-

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

if __name__ == '__main__':
    try:
        with connection.cursor() as cursor:
            # sql = 'create table if not exists type(movie_type varchar(1000),name varchar(1000),diretor varchar(1000),star varchar(1000),' \
            #                       'score varchar(1000),runtime varchar(1000),' \
            #                   'date varchar(1000),area varchar(1000),type varchar(1000),url varchar(1000))'  # 创建表
            # cursor.execute(sql)
            sql = 'select * from douban'
            cursor.execute(sql)
            infors = cursor.fetchall()

            ListForType = []
            for ss in infors:
                slist = ss['type'].split(',')
                for sl in slist:
                    if sl and (sl not in ListForType):
                        ListForType.append(sl)
            sql = "replace into type values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
            for ll in ListForType:
                for ss in infors:
                    slist = ss['type'].split(',')
                    for sl in slist:
                        if sl == ll:
                            cursor.execute(sql % (ll,ss['name'],ss['diretor'],ss['star'],ss['score'],ss['runtime'],ss['date'],ss['area'],ss['type'],ss['url']))
                print 'ok...'
            print 'yes...'
            connection.commit()            # 提交数据
            cursor.close()                 # 关闭游标
    finally:
        connection.close()             # 关闭连接
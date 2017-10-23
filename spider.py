#!/usr/bin/env python
#coding:utf-8

import douban
import pymysql
import pymysql.cursors

config = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'passwd':'654321',
    'db':'douban_database',
    'use_unicode':1,
    'charset':'utf8',
    'cursorclass':pymysql.cursors.DictCursor          # 以字典形式返回,默认是元组
}
connection = pymysql.Connect(**config)

if __name__ == '__main__':
    try:
        doubanSp = douban.DouBanMovieSpider(connection)
        doubanSp.spider()
    except Exception as err:
        print 'fail to spider-->',err
        connection.close()
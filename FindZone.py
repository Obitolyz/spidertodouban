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

if __name__ == '__main__':
    try:
        with connection.cursor() as cursor:
            sql = 'select * from zone'
            cursor.execute(sql)
            infors = cursor.fetchall()

            ListForArea = []
            sql = "update zone set area='%s' where area='%s'"
            for ss in infors:
                sarea = ss['area'].replace(' ','').split('/')   # 去掉多余的空格然后切分开来(ps:存数据的时候忘记处理空格了)
                for el in range(len(sarea)):
                    # print el,
                    sarea[el] = filter(lambda c : u'\u4e00' <= c <= u'\u9fa5',sarea[el])   # 去掉非中文字母(这里是为了去掉英文字母)
                    # print newel
                    # 将繁体字转化为简体字   other(Converter('zh-hant').convert(newel)
                    sarea[el] = Converter('zh-hans').convert(sarea[el])
                    # if not newel2:
                    #     print newel,el,ss['name'],'|',ss['area']     # 测试数据
                    if sarea[el] not in ListForArea:
                        # if newel2 != u'印尼':         # 非得加个u,变成unicode,涨姿势了
                        ListForArea.append(sarea[el])
                ll = '/'.join(sarea)
                # print ll
                cursor.execute(sql % (ll,ss['area']))
                # print 'ok...'

            # # 处理地区
            # fp = open('D:/PycharmProjects/_datasheets/test_zone.txt','w')
            # json.dump(ListForArea,fp,ensure_ascii=False)         # ,ensure_ascii=False
            # fp.close()

            # fp = open('D:/PycharmProjects/_datasheets/test_zone.txt','r')
            # json.load(fp)
            # fp.close()

            # for ll in ListForArea:
            #     if ll:
            #         print ll,
            #     else:
            #         print 'nothing...'
            # print '\n',len(ListForArea)

            print 'ok...'
            connection.commit()            # 提交数据
            cursor.close()                 # 关闭游标
    finally:
        connection.close()             # 关闭连接
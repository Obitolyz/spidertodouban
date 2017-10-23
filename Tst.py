#!/usr/bin/env python
#-*- coding=utf-8 -*-

import pymysql
import pymysql.cursors
import time
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
con_sql = pymysql.Connect(**config)
cursor = con_sql.cursor()
username = 'user3'
sql = "select * from user where %s=1"
cursor.execute(sql % username)
infors = cursor.fetchall()

res = dict()

for fs in infors:
    for key in fs:
        if key != 'name' and key != username:   # 除掉Movie和当前用户
            if key in res:
                res[key] += fs[key]
            else:
                res[key] = fs[key]

for rs in res:
    print rs,res[rs]

res_name = sorted(res,key=lambda e: res[e],reverse=True)[:3]
print res_name
# sql = "update user set %s=1 where name='%s'"
# cursor.execute(sql % (username,'莹仔'))
sql = "select name from user where %s=1"
cursor.execute(sql % username)
print cursor.fetchall()

if __name__ == '__main__':
    con_sql.commit()
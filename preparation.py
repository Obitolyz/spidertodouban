#!/usr/bin/env python
#coding=utf8

import os
os.remove(path)      # 删除指定路径的文件
fp = open(path,'w')       # 新建文件     fp.close()

# sql = 'create database database_name'   # 创建数据库      # show databases/tables;
# 'drop database/table if exists database_name/table_name'           # 删除数据库/表
# cursor.execute(sql)
# sql = 'use database_name'               # 使用数据库
# cursor.execute(sql)

# sql = 'create table if not exists table_name(name varchar(18),score varchar(18))'     # 创建表
# cursor.execute(sql)
# sql = "insert into user(name,password) values('%s','%s')"     # 插入数据
# sql = "update user set ... where ..."    # 更新数据
# sql = "delete from user where ..."       # 删除数据
# cursor.executemany(sql,[...])            # 插入多条数据
# select name,password from user where name = '' and password = ''


# cursor.scroll(pos,'absolute') 游标回到表中的第一个数据   'relative':代表相对位置   'absolute':代表绝对位置
# print cursor.rowcount    # 返回执行execute()方法后影响的行数。
# print cursor.lastrowid    # 好像是插入数据后的
# cursor.fetchmany(n)       # 取出n条数据

# 'alter table table_name rename table_new_name'        # 修改表的名字

# 复制表
# create table douban2 like douban                    # 拷贝表结构
# insert into (database.)douban2 select * from douban  # 可以从不同的数据库

# create table douban2 select * from douban

# 更改列类型
# alter table employee modify column truename varchar(10) NOT NULL DEFAULT ''

# 更改列名
# alter table 表名 modify 列名 新类型 新参数【修改列类型】
# 例：alter table test modify gender char(4) not null default '';
# alter table 表名 change 旧列名 新列名 新类型 新参数【修改列名和列类型】
# 例：alter table test change pid uid int unsigned not null default 0;

# 添加主键
# alter table 表名 add primary key(id)

# show create table 表名【查看表的创建代码】

# 增加列[add 列名]
# =========================
# alter table 表名 add 列名 列类型 列参数【加的列在表的最后面】
# 例：alter table test add username char(20) not null default '';
#    alter table test add birth date not null default '0000-00-00';
#
# alter table 表名 add 列名 列类型 列参数 after 某列【把新列加在某列后面】
# 例：alter table test add gender char(1) not null default '' after username;
#
# alter table 表名 add 列名 列类型 列参数 first【把新列加在最前面】
# 例：alter table test add pid int not null default 0 first;
#
# =========================
# 删除列[drop 列名]
# =========================
# alter table 表名 drop 列名
# 例：alter table test drop pid;
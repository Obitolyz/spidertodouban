#!/usr/bin/env python
#coding=utf-8

# import database as db
# from langconv import *
import time
import sys
import copy
reload(sys)
sys.setdefaultencoding('utf8')        # 这个就很厉害了，设置默认编码

# con_sql = db.connection
# cursor = con_sql.cursor()
# cursor.execute('select * from system_douban')
# allinfors = cursor.fetchall()        # is a list

# ratio = {u'导演':1,u'演员':1,u'类型':2,u'地区':1}        # 各标签的权值修改
# flag = [u'导演',u'演员',u'类型',u'地区']

class NewRecommend(object):

    def __init__(self):
        self.LikeLables = dict()
        self.watched = list()  # [{},{},...]
        self.LimitTime = 7 * 24 * 3600   # 标签的有效期为一周
        self.ratio = {u'导演':1,u'演员':1,u'类型':2,u'地区':1}        # 各标签的权值修改
        self.flag = [u'导演', u'演员', u'类型', u'地区']

    def learn(self,info):   # info是[[导演],[演员],[类型],[地区]]           还有权值weight
        n = 0
        for io in info:
            for ll in io:
                if ll:    # 不为空
                    if ll not in self.LikeLables:
                        self.LikeLables[ll] = (1,time.time(),self.flag[n])
                    else:
                        self.LikeLables[ll] = (self.LikeLables[ll][0]+1,time.time(),self.flag[n])
            n += 1

    def GetRecommendResult(self,allinfors):    # 基于物品的推荐(除了已经看过的电影)
        # 去掉失效的标签
        if len(self.LikeLables) == 0:
            return []
        # 去掉已经看过的电影
        for w in self.watched:
            if w in allinfors:
                allinfors.remove(w)

        nt = time.time()     # 现在的时间
        # 去掉失效的标签
        dpc = copy.deepcopy(self.LikeLables)
        for ll in self.LikeLables:
            if nt - self.LikeLables[ll][1] >= self.LimitTime:
                del dpc[ll]
        self.LikeLables = copy.deepcopy(dpc)

        # 取10个系数最高的标签 类型:2 导演:3 演员:3 地区:2  这个可以修改
        favor_lable = []
        rs = sorted(self.LikeLables,key=lambda e: (self.LikeLables[e][2] == '导演')*self.LikeLables[e][0],
                    reverse=True)[:3]   # 从高到低排
        favor_lable.extend(rs)
        rs = sorted(self.LikeLables, key=lambda e: (self.LikeLables[e][2] == '类型') * self.LikeLables[e][0],
                    reverse=True)[:2]
        favor_lable.extend(rs)
        rs = sorted(self.LikeLables, key=lambda e: (self.LikeLables[e][2] == '地区') * self.LikeLables[e][0],
                    reverse=True)[:2]
        favor_lable.extend(rs)
        rs = sorted(self.LikeLables, key=lambda e: (self.LikeLables[e][2] == '演员') * self.LikeLables[e][0],
                    reverse=True)[:3]
        favor_lable.extend(rs)
        favor_lable = list(set(favor_lable))

        res = dict()                      # 创建一个字典,这就很厉害了...
        tot = len(allinfors)
        for index in range(tot):
            res[index] = 0
            ssr = []          # 存放一部电影的有效标签
            # 添加导演进去
            ssr.append(allinfors[index]['diretor'])
            # 添加演员进去
            star = allinfors[index]['star'].split(',')   # 拆分为列表
            ssr.extend(star)     # 合并列表
            # 添加类型进来
            type = allinfors[index]['type'].split(',')
            ssr.append(type)
            # 添加地区进来
            # area = AllData[index]['area'].replace(' ','').split('/')
            # for n in range(len(area)):
            #     area[n] = filter(lambda c: u'\u4e00' <= c <= u'\u9fa5',area[n])   # 去掉非中文字符
            #     area[n] = Converter('zh-hans').convert(area[n])       # 转化为简体字
            area = allinfors[index]['area'].split('/')
            ssr.append(area)

            for like in favor_lable:
                if like in ssr:
                    res[index] += self.LikeLables[like][0] * self.ratio[self.LikeLables[like][2]]  # 权值weigh

        seq = sorted(res,key=lambda x:res[x],reverse=True)[:30]        # 得到的是键 sorted保留原来的数据
        # 筛选出30部电影,然后再选出评分最高的10部电影
        # sorted(iterable, cmp=None, key=None, reverse=False)
        result = []
        for ii in seq:
            result.append(allinfors[ii])      # 得到的是[{},{},...]
        return sorted(result,key=lambda x: float(x['score']),reverse=True)[:10]     # 推荐的电影[{},{},...]
        # sorted(result,cmp=lambda x,y:cmp(x['score'],y['score']),reverse=True)

    def save(self,cursor,username,con_sql):
        cursor.execute('truncate table %s_lables' % username)   # 相当于将表删除后重建,效率比delete快    delete from table_name (where...)
        sql = "replace into %s_lables values('%s','%d','%d','%s')"
        for lls in self.LikeLables:
            cursor.execute(sql % (username,lls,self.LikeLables[lls][0],self.LikeLables[lls][1],self.LikeLables[lls][2]))
        sql = "replace into %s_watched values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"
        for w in self.watched:
            cursor.execute(sql % (username,w['name'],w['diretor'],w['star'],
                                  w['score'],w['runtime'],w['date'],w['area'],w['type'],w['url']))
        con_sql.commit()                 # 记住一定要提交,不然数据没法上传...坑过一次,,,呜呜呜~~~

    def load(self,cursor,username):
        sql = 'select * from %s_lables'
        cursor.execute(sql % username)
        lls = cursor.fetchall()
        for ls in lls:
            self.LikeLables.update({ls['lable']:(ls['times'],ls['save_time'],ls['type'])})
        sql = 'select * from %s_watched'
        cursor.execute(sql % username)
        self.watched = list(cursor.fetchall())   # 强制转换为列表

# if __name__ == '__main__':
#     User = NewRecommend()
#     User.load(cursor,"莹仔")
#     User.save(cursor,"莹仔",con_sql)
#     cursor.close()
#     con_sql.close()
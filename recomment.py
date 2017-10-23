#!/usr/bin/env python
#coding:utf-8

import time
import json
import copy

class Recomment(object):

    def __init__(self):
        self.LikeLables = dict()
        self.LimitTime = 7*24*3600
        self.saveDir = 'D:/PycharmProjects/_datasheets/LikeLable.txt'

    def learn(self,infor):    # infor:电影,提取里面的标签(导演str,主演[str],类型[str])
        if infor['diretor'] not in self.LikeLables:
            self.LikeLables[infor['diretor']] = (1,time.time())
        else:
            self.LikeLables[infor['diretor']] = (self.LikeLables[infor['diretor']][0]+1,time.time())

        lable = ['star','type']
        for ll in lable:
            for el in infor[ll]:
                if el in self.LikeLables:
                    self.LikeLables[el] = (self.LikeLables[el][0]+1,time.time())
                else:
                    self.LikeLables[el] = (1,time.time())

    # test_infor[str]
    def get_recommend_result(self,test_infor,number=5):            # 注意0的情况
        if len(self.LikeLables) == 0:
            return []
        t = time.time()
        # 去掉失效的标签
        dp = copy.deepcopy(self.LikeLables)
        for ll in self.LikeLables:
            if t - self.LikeLables[ll][1] >= self.LimitTime:
                del dp[ll]
        self.LikeLables = copy.deepcopy(dp)
        # key_list:整理好数据再放进去
        res = dict()
        key_list = sorted(self.LikeLables, key=lambda x: self.LikeLables[x][0], reverse=True)  # 得到的是标签(str)
        if len(key_list) >= 5:
            key_list = key_list[:5]  # 取5个最高的标签出来
        for index in range(len(test_infor)):
            res[index] = 0
            # 分解标签
            ssr = []
            ssr.append(test_infor[index]['diretor'])
            label = ['star','type']
            for x in label:
                for y in test_infor[index][x]:
                    ssr.append(y)

            for like in key_list:
                if like in ssr:
                    res[index] += 1
        return sorted(res,key=lambda x:res[x],reverse=True)[1:number+1]


    def save(self):
        fp = open(self.saveDir,'w')
        json.dump(self.LikeLables,fp,ensure_ascii=False)
        fp.close()

    def load(self):
        fp = open(self.saveDir,'r')
        self.LikeLables = json.load(fp)
        fp.close()
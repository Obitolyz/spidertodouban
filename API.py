#!/usr/bin/env python
#coding:utf-8

import json
import glob
import os      # os.mkdir os.rmdir
from recomment import Recomment
from time import sleep
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


paths = glob.glob('D:/PycharmProjects/data*/*.txt')
Json_List = []

for path in paths:
    fp = open(path,'r')
    Json_List.append(json.load(fp))
    fp.close()

def display(ds):
    print '导演:%s' % ds['diretor']
    print '主演:',
    for ss in ds['star']:
        print ss,
    print ''
    print '评分:%s' % ds['score']
    print '链接:%s' % ds['url']

app = Recomment()
save_ds = []

# fp = open('D:/PycharmProjects/_datasheets/all.txt','w')    # 整合成一个文件
# for ss in Json_List:
#     object_to_string = json.dumps(ss,ensure_ascii=False)
#     fp.writelines(object_to_string + '\n')
# fp.close()

# fp = open('D:/PycharmProjects/_datasheets/all.txt','r')   # 从文件中提取出来
# for line in fp:                                               # 一行一行遍历文件,得到字符串,然后解析成对象
#     res = json.loads(line)
# fp.close()

if __name__ == '__main__':
    while True:
        tot = 0
        flag = 1
        save_ds = []
        try:
            name = raw_input('>>>')
            if name == '猜我喜欢':
                app.load()
                rs = app.get_recommend_result(Json_List)
                for r in rs:
                    print Json_List[r]['name']

            else:
                for ds in Json_List:
                    if name == ds['name']:     # 为什么is不行(for is是根据id来判断的)
                        display(ds)
                        app.learn(ds)       # 学习标签
                        app.save()
                        flag = 0
                        break
                    else:
                        if name != '' and name in ds['name'].replace(' ',''):    # replace()
                            save_ds.append(ds)
                            tot += 1
                if tot:
                    print '为你找到%d部电影...' % tot
                    for el in save_ds:
                        print el['name']
                else:
                    if flag:
                        print '没找到匹配的电影...'

        except Exception:
            pass


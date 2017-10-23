#/usr/bin/env python
#coding:utf-8

import requests
import re
from time import sleep

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

lables = ['热门','最新','经典','可播放',
         '豆瓣高分','冷门佳片','华语','欧美',
         '韩国','日本','动作','喜剧','爱情',
         '科幻','悬疑','恐怖','治愈'
]

# page_start:表示前面有多少个链接
url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=热门&sort=recommend&page_limit=20&page_start=0'
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text
# pat = '"url":"https:\/\/movie.douban.com\/subject\/(\d{8})\/"'   # 不懂为什么爬不了
pat = '"url":"(.*?)"'

if __name__ == '__main__':
    res = re.findall(pat,html)
    for index in range(len(res)):
        res[index] = res[index].replace('\\','')    #

    for ss in res:
        sleep(1)
        response = requests.get(ss)
        response.encoding = 'utf-8'
        html = response.text
    # fp = open('/home/wuguojin/Desktop/yz.txt','w')
    # for s in html:
    #     fp.write(s)
    print 'done...'
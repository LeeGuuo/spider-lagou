import re
import time
import requests
import pandas as pd
from retrying import retry
from concurrent.futures import ThreadPoolExecutor

for i in range(1, 2):
    j = 44 * (i-1)

def network_programming(num):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/75.0.3770.100 Safari/537.36'}
    url = 'https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2\
           &sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E6%B2%99%E5%8F%91&suggest=history_1\
           &_input_charset=utf-8&wq=&suggest_query=&source=suggest&fs=1&is618=1&filter=reserve_price%5B500%2C%5D\
           &bcoffset=-3&p4ppushleft=%2C44&s=' + str(num)
    web = requests.get(url=url, headers=headers)
    web.encoding = 'gbk'
    web = web.text
    return web


data = network_programming(j)
print(data)


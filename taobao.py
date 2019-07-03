import re
import time
import requests
import pandas as pd
from retrying import retry
from concurrent.futures import ThreadPoolExecutor
'''
spider donot work  how
'''
start = time.clock()

plist = []
for i in range(1, 2):
    j = 44 * (i-1)
    plist.append(j)

listno = plist
datatmsp = pd.DataFrame(columns=[])

while True:
    # 设置最大重试次数
    @retry(stop_max_attempt_number=3)
    def network_programming(num):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/75.0.3770.100 Safari/537.36'}
        url = 'https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2\
               &sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E6%B2%99%E5%8F%91&suggest=history_1\
               &_input_charset=utf-8&wq=&suggest_query=&source=suggest&fs=1&is618=1&filter=reserve_price%5B500%2C%5D\
               &bcoffset=-3&p4ppushleft=%2C44&s=' + str(num)
        web = requests.get(url=url, headers=headers)
        web.encoding = 'utf-8'

        return web

    # 多线程
    def multithreading():
        # 每次爬取未成功的页
        number = listno
        event = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            for result in executor.map(network_programming, number, chunksize=10):
                event.append(result)

        return event

    listpg = []
    event = multithreading()
    for i in event:
        json = re.findall('"auctions":(.*?),"recommendAuctions"', i.text)
        if len(json):
            table = pd.read_json(json[0])
            datatmsp = pd.concat([datatmsp, table],axis=0,ignore_index=True)
            pg = re.findall('"pageNum":(.*?),"p4pbottow_up"', i.text)[0]
            # 记录每一次爬取成功的页
            listpg.append(pg)

    lists = []
    for a in listpg:
        b = 44 * (int(a) - 1)
        # 将爬取成功的页码转为url中的num 值
        lists.append(b)

    listn = listno
    # 将本次爬取失败的页计入列表中，用于循环爬取
    listno = []
    for p in listn:
        if p not in lists:
            listno.append(p)
    # 当未爬取页数为0时，终止循环
    if len(listno) == 0:
        break

datatmsp.to_csv('datatmsp.csv', index=False)
end = time.clock()
times = str(end - start)
print("用时:%s" % times, 's')


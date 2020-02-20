"""
@File        : 01.py
@Description : JS逆向第一关，JSFuck的解决
解决JSFUCK的一串被改动过的代码很简单，把这一串代码复制到谷歌提供的开发工具，也就是右键点击一个和要
解析的页面不相关的页面然后点Source,在console里面输入console.log(jsfuck代码)，因为这个页面是
不相关的，它会报错，然后点击VM**就会跳转到一个文件，那个文件的内容就是JSFuck里被转化的内容！
@author      : sheng
@date time   : 2019/11/14 14:00
@version     : v1.0
"""
import hashlib
import math
import random
import time
from functools import reduce
import requests

user_agents = []

headers = {
    "Cookie": "_ga=GA1.2.314768685.1574439176; "
              "_gid=GA1.2.1883924923.1574439176; "
              "Hm_lvt_020fbaad6104bcddd1db12d6b78812f6=1574448401,1574448970,"
              "1574449574,1574467956; _gat_gtag_UA_75859356_3=1; "
              "footprints=eyJpdiI6ImRRSlZKZnc1K0pWOXVNYWloQndwTUE9PSIsInZhbHVlIjoiZkRlRENJS1JuWmIrT0JZZk5ZMkJNRkdkVXdIdWxsZU1TdTBXZThBemZFK3drN2xFSXJuZmdCakJWNm9NTWpOWCIsIm1hYyI6IjA2MTQxNTJmMWIyOGUzMTVhMTNhOWY1OTk2NTgyOTA3ZGJhMTQ5ODc1NTJiYWFhODExOGM5MDgxNTg1YWRhNDIifQ%3D%3D; Hm_lpvt_020fbaad6104bcddd1db12d6b78812f6=1574467984; XSRF-TOKEN=eyJpdiI6Inc1WGNRbXQ5VHJsVXRLQ2Nic3ZUTGc9PSIsInZhbHVlIjoiZ3RCdFpmUWtyUHZTSUhubU1aYVliWW5obDI4dFNvYWo4Ykp6RnV5Y3lcL0tLZEhMS1wvR1VEd1UrVFBzNkl2SXZvIiwibWFjIjoiMWUzNGFiNGMyYmFlNjViNTRiODE1YjE4ZGU4ZGMyZThhNDU0NmVlZTZjNjNjZjU2ZjI0M2Q1NjU1ZGJmMzliYiJ9; glidedsky_session=eyJpdiI6IjFqR1JyQ0czTnlEcTBhVG5XR3loUHc9PSIsInZhbHVlIjoiaGg1SzYyWDJ5eUZNNEY1dEVwb0dRNk1obEl4aHNpR0pVMmpWdllSNzN3MHlnSHNUaHhlakdNNkg4UjZKdzNoKyIsIm1hYyI6ImZmZmFiOTI1YzU2N2Q2M2U2YWUxNjQyNjgzZGY2NThkMzdkN2QyNTc0NjAwNDA0MDNiNmRmMjliZTNmYjUwOGIifQ%3D%3D",
    "Referer": "http://glidedsky.com/level/web/crawler-javascript-obfuscation-1"
               "-1",
    "Accept": "*/*",
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/78.0.3904.108 Safari/537.36',
    'Connection': 'keep-alive',
    'Host': 'glidedsky.com',
    'Accept-Encoding': 'gzip, deflate',
    'Upgrade-Insecure-Requests': '1'
}
sum = 0
for page in range(1, 1001):
    try:
        print(f'这是第{page}页')
        t = timestamp = math.floor((int(round(time.time() * 99)) - 99) / 99)
        sha = hashlib.sha1(
            ('Xr0Z-javascript-obfuscation-1' + str(t)).encode('utf-8'))
        sign = sha.hexdigest()
        # page = 2
        url = f'http://glidedsky.com/api/level/web/crawler-javascript-obfuscation' \
              f'-1' \
              f'/items?page={page}&t={t}&sign={sign}'
        response = requests.get(url=url, headers=headers, timeout=5)
        sum += reduce(lambda x, y: x+y, response.json()['items'])
        # time.sleep(random.randint(1, 3))
        print(print(sum))
    except TypeError: # 由于速度太快可能得到的返回值类型不是integer导致报错，一旦捕获再发送相同请求就好
        print(f'这是第{page}页')
        t = timestamp = math.floor((int(round(time.time() * 99)) - 99) / 99)
        sha = hashlib.sha1(
            ('Xr0Z-javascript-obfuscation-1' + str(t)).encode('utf-8'))
        sign = sha.hexdigest()
        # page = 2
        url = f'http://glidedsky.com/api/level/web/crawler-javascript' \
              f'-obfuscation' \
              f'-1' \
              f'/items?page={page}&t={t}&sign={sign}'
        response = requests.get(url=url, headers=headers, timeout=5)
        sum += reduce(lambda x, y: x + y, response.json()['items'])
        # time.sleep(random.randint(1, 3))
        print(print(sum))

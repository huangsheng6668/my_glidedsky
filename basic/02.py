"""
@File        : 02.py
@Description : 镀金的天空，爬虫第二关
@author      : sheng
@date time   : 2019/11/12 13:20
@version     : v1.0
"""
import time

import requests
from lxml import etree
from lxml.etree import HTMLParser

headers = {
    "Cookie": "_ga=GA1.2.1402170177.1572708270; "
              "Hm_lvt_020fbaad6104bcddd1db12d6b78812f6=1572708270,1573196621,"
              "1573522309; _gid=GA1.2.257950389.1573522310; "
              "footprints=eyJpdiI6IkdcL082ZkMzQWFvTXQ1dTFJcXdHNFwvdz09IiwidmFsdWUiOiJvQk9EbkIxUml0WGJtNzlBdFNJK3dLK3NQWGE5M3FRTGg0MzUrdlBJck9TMStXaXo3NDRKTmZGNndzS2FcL0pXcyIsIm1hYyI6ImExZWM2NWQ0NWM4OWFjNGYwMWYyNzU4MzA1MDhmNjg2YzJlM2RiN2ZiNGE3NTFhMTg5NWYyYmY3OTc2YzY0NjgifQ%3D%3D; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6ImdWSlFSeGE1YmZoV1NNNjg2T0RkTlE9PSIsInZhbHVlIjoic2xHNFNBdTRPODZxNlwvMUQwbVwva0VHWlErRDEwMVRGWDBmV1RNclRsYVFHOHRUVHE2cTl6MWpcL0VnNjRHdFBiaVhsS1lsWUFMRm5wV2dEWGJPRzRPNHBCUkJQMFZvS0lRQ0x1V0RQV01ETWUwZXFZc3ZOV0V6S3plMmY0SjJIcHoydGpKdUg2aG5HYUZcL3kzd2hnZ3Vaam4xejBmbkw1SlYrTUo3N3k4ZlRlST0iLCJtYWMiOiIxMzAxODk0NGRkZTg3ZDhiNjFjYzEyMzgyMTI5YjBiNGZkZDI0MmNlZTliYzg1OGZjMWU4NDYxZDBlOTI3NTY0In0%3D; XSRF-TOKEN=eyJpdiI6InBDVVdJaGRNWjUxcVVzMHdkNVppcXc9PSIsInZhbHVlIjoiYm1iMXk3YWFBQWwrcVViRHA0MVhtb3ZwYTBmZmY3YWJTcFJCTVhhbWQyTitRczF5WG5oQmNrQ3Nka3VBSGN0ZyIsIm1hYyI6IjAzNGNiMjIyOTVmZTE2ZjBmMTgwOTMxNjZkMTVkOWZlMTAzNzUwOTA0N2QyNGYzMzllZTc2YzZiZTBmNGM3ZGUifQ%3D%3D; glidedsky_session=eyJpdiI6IkdTayt6K05CVmc3clNybGh3TnBQWnc9PSIsInZhbHVlIjoiUlB5MkpNN2c0UFpNNEZMRGhNTGoyNXdtVnZCODRRSGNMdVYwalFvbjhcL2N1OGlPWWtkaEI5ZW9Od0FZaTh3YzkiLCJtYWMiOiJlY2NhZThhZmIyMGZiODU0ZmJjY2Y5OTVkYTkyYTBmYWRlYzdmNWJhMWNjZDM0YWI5M2I0NjRiNmI5ZjdlYmEwIn0%3D; Hm_lpvt_020fbaad6104bcddd1db12d6b78812f6=1573523456",
    "Referer": "http://glidedsky.com/level/crawler-basic-2",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
}
num_list = []
sum = 0
for page in range(1, 1001):
    print(page)
    rep = requests.get(
        url=f'http://www.glidedsky.com/level/web/crawler-basic-2?page={page}',
        headers=headers)
    html = etree.HTML(rep.text, HTMLParser())
    items = html.xpath(
        "//*[@id='app']/main/div/div[@class='card']/div[@class='card-body']/div[@class='row']//div[@class='col-md-1']/text()")
    for i in items:
        num_list.append(int(i.strip()))
for i in num_list:
    sum += i
print(sum)

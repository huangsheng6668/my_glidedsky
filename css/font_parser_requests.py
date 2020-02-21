#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File       :   font_parser_requests.py
@Email      :   huangsheng6668@163.com
@Modify Time:   2020/2/20 10:12
@Author     :   sheng
@Version    :   1.0
@Description:   None
"""
import re
import os
from fontTools.ttLib import TTFont
import requests

"""
登录glidedSky,获取session
"""


def login(user_email: str, user_password: str):
    global session
    session = requests.session()

    def get_token():
        html = session.get('http://glidedsky.com/').text
        _token = re.search(
            '<input type=\"hidden\" name=\"_token\"\s?value="(.*?)"',
            html).group(1)
        return _token

    def post_data(user_email, user_password):
        data = {
            'email': user_email,
            'password': user_password,
            '_token': get_token()
        }
        header = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) '
                          'AppleWebKit / 537.36(KHTML, likeGecko) Chrome / '
                          '80.0.3987.100Safari / 537.36',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,'
                               'en-US;q=0.3,en;q=0.2',
            "Content-Type": "application/x-www-form-urlencoded",
            'Accept': '"application/json, text/plain, */*"'
        }
        session.headers = header
        session.post(url='http://glidedsky.com/login', data=data)

    post_data(user_email, user_password)


"""
获取当前页的源码当中的数字以及字体文件
"""


def get_page(page: int):
    from parsel import Selector
    import base64

    html = session.get(f'http://glidedsky.com/level/web/crawler-font-puzzle-1?page'
                       f'={page}').text
    select = Selector(text=html)
    style = select.css('style')
    base64_url = style.re_first('.*base64,(.*?)\) format')
    font_family = base64.b64decode(base64_url)
    with open(f'glided_sky{page}.ttf', 'wb') as f:
        f.write(font_family)
    nums = []
    for div in select.css('.col-md-1'):
        nums.append(div.xpath('.//text()').re_first('\n\s*\r*(\d+)'))
    save_font_family_xml(page)
    return nums


"""
保存字体文件为xml形式
"""


def save_font_family_xml(page: int):
    font_xml_name = f'glided_sky{page}.xml'
    font_path_name = f'glided_sky{page}.ttf'
    font = TTFont(font_path_name)
    font.saveXML(font_xml_name)


"""
解析生成的xml文件
"""


def parse_for_xml(file_path: str, nums: list) -> list:
    from xml.dom.minidom import parse

    dom_tree = parse(file_path)
    root = dom_tree.documentElement
    mapping_num_dict = {}
    all_children = root.getElementsByTagName('GlyphID')
    # 字体文件当中，0对应的那一行对应的name不为数字，且10不存在，我们把0后面的name依次往前替换上一个的
    # name,比如0对应的那行的name的下一个name为one则0对应one
    for index, child in enumerate(all_children):
        if index == len(all_children) - 1:
            break
        mapping_num_dict.setdefault(str(index), all_children[index + 1].getAttribute(
            'name'))
    # 循环后值对应的键即为相应的显示的值
    for idx, value in enumerate(mapping_num_dict.values()):
        mapping_num_dict[str(idx)] = mapping_num()[value]
    # 翻转键值
    mapping_num_dict = dict([[value, key] for key, value in mapping_num_dict.items()])
    # 求出该页正确的数字列表
    for idx, num in enumerate(nums):
        real_num = ''
        for i in num:
            real_num += mapping_num_dict[i]
        nums[idx] = int(real_num)
    return nums


"""
真实的映射字典
"""


def mapping_num() -> dict:
    dict_num = {
        'zero': '0',
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }
    return dict_num


"""
删除本次循环产生的文件
"""


def remove_font_file(file_name: str):
    file_path = os.getcwd() + r'\\' + file_name
    if os.path.exists(file_path):
        os.remove(file_path)


if __name__ == '__main__':
    login('', '')
    answer = 0
    for page in range(1, 1001):
        nums = get_page(page)
        font_xml_name = f'\\glided_sky{page}.xml'
        font_path_name = f'\\glided_sky{page}.ttf'
        num_list = parse_for_xml(os.getcwd() + font_xml_name, nums)
        for num in num_list:
            answer += num
        print('第', str(page), '页:' + str(answer))
        add_file_paths = [font_xml_name, font_path_name]
        # map外面如果不加list，map返回的是一个map类，并没有执行里面的函数
        list(map(remove_font_file, add_file_paths))

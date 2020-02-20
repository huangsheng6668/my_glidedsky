"""
@File        : login_glidedsky.py
@Description : 登录glidedSky
@author      : sheng
@date time   : 2020/2/12 16:42
@version     : v1.0
"""
import re

import requests


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
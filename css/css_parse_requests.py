"""
@File        : css_parse_requests.py
@Description : 用requests解决CSS反爬
@author      : sheng
@date time   : 2020/2/12 16:56
@version     : v1.0
"""
import re
import requests
from parsel import Selector


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


# 获取页面
def get_html(user_name: str, user_password: str, url: str) -> str:
    login(user_name, user_password)
    html = session.get(url=url)
    return html.text


# 解析页面
def parse_html(html: str, offset_element_list, unexist_div_classes):
    selector = Selector(html)
    all_div = selector.xpath(r'//div[@class="row"]//div[@class="col-md-1"]')
    nums = []
    for index, divs in enumerate(all_div):
        # 遍历每个col-md-1中的div
        # 用于存储偏移的元素
        num = {}
        for idx, div in enumerate(divs.xpath('./div')):
            cur_div_class = div.xpath('./@class').extract_first()
            # 当这个元素为不显示的元素则跳过
            offset_element_list.sort(key=lambda x: x[0] != cur_div_class)
            if cur_div_class in unexist_div_classes:
                continue
            # 当这个元素存在偏移值时，算出真正下标添加进字典里
            elif cur_div_class == offset_element_list[0][0]:
                    real_index = idx + int(offset_element_list[0][1])
                    num[str(real_index)] = div.xpath('./text()').extract_first()
            else:
                # 元素没有设置反爬，正常获取
                if div.xpath('./text()').extract():
                    num.setdefault(str(idx), div.xpath('./text()').extract_first())
        # 给字典排序并转换为列表，转成后的格式为list[(key, value)]，使得键值按顺序排列，方便后续的遍历直接遍历
        # x[0]为按键值排序，x[1]为按值排序
        num = sorted(num.items(), key=lambda x: x[0], reverse=False)
        temp = ''
        # 遍历列表，给定一个临时变量，然后遍历列表，添加，后续一转换就可以了
        for i in num:
            temp += str(i[1])
        nums.append(temp)
    return nums


# 找出所有通过偏移元素达到反扒效果的类名和值
def offset_element(html: str) -> list:
    return re.findall('\.(.*?)\s?\{\s?\n?\r?left:(-?\d*)em\s?\s?\n?\r?\}', html)


# 找出所有带有伪类的div的conten值
def fake_div(html: str) -> list:
    return re.findall(
        '\.(.*?):before\s?\{\s?\n?\r?content:\s?\"(\d*)\s?\"\s?\n?\r?\}', html)


# 找出所有不显示的div，观察参数可得知margin-right=-1的为不显示的参数
def unexist_div(html: str) -> list:
    return re.findall('\.(.*?)\s?\{\s?\n?\r?margin-right:-\d.*?}', html)


if __name__ == '__main__':
    import time
    # 账号
    user_name = ''
    # 密码
    user_password = ''
    answer = 0
    for page in range(1, 1001):
        url = f'http://glidedsky.com/level/web/crawler-css-puzzle-1?page={page}'
        html = get_html(user_name=user_name, user_password=user_password, url=url)
        # 获取所有带有伪类的标签中伪类的content值
        fake_div_values = fake_div(html)
        # 找出所有通过偏移元素达到反扒效果的类名和值
        offset_element_list = offset_element(html)
        # 找出所有不显示的元素
        unexist_div_classes = unexist_div(html)
        # 获取所有通过偏移元素改变爬取效果的真实值
        offset_real_list = parse_html(html, offset_element_list,
                                      unexist_div_classes)
        # 把所有结果添加起来
        for i in fake_div_values:
            answer += int(i[1])
        for i in offset_real_list:
            if i:
                answer += int(i)
        print('页数:' + str(page) + '总计' + str(answer))

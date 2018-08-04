# coding:utf-8
import csv

import pandas as pd
from bs4 import BeautifulSoup
import urllib

from pip._vendor.urllib3 import request


def get_html(url):
    page = urllib.urlopen(url)  # 打开网页
    return page.read()  # 读取页面源码


def write_csv(list):
    columns = ['药品名', '产品规格', '生产厂家', '零售价']
    csvfile = pd.DataFrame(columns=columns, data=list)  # 打开方式还可以使用file对象
    csvfile.to_csv('云药库(登录).csv', index=False, encoding='GBK')


def get_total_page():
    html = get_html('http://www.xty999.com/productlist.ac?row=y&&category=1&&order=salesVolume%2Cdesc&page=1')
    # html = get_html('http://127.0.0.1:5500/html/index.html')
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find('div', {'class': 's-pager'})
    span_array = div.findAll('span')
    span = span_array[1].text
    span = span[1:len(span)]
    span = span[:-1]
    return span


def get_spider(url):
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    loginId = soup.find('input', {'id': 'loginId'})


def get_code(url):
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    img = soup.find('img', {'id': 'validateCodeImg'})
    src = img['src']
    urllib.urlretrieve('http://www.xty999.com' + src, 'code.png')


loginHtml = 'http://www.xty999.com/login.ac'
codeImg = 'http://www.xty999.com/ValidateCode'
loginId = '15876541676'
userPsw = '21cdc7f6e4cdb7fbe9b80fa8c1908f8d'
validateCode = ''

data = {
    'loginId': loginId,
    'userPsw': userPsw,
    'validateCode': True
}

# 模拟登录
response = request.getSession().post(login_url, data=json.dumps(data))
get_spider(loginHtml)

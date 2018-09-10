# coding:utf-8

import pandas as pd
from bs4 import BeautifulSoup
import urllib
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def get_html(url):
    cookies = 'PHPSESSID=it3q07hcnjhc5rh22bo0545qo0; Hm_lvt_4a001c429a59102d2d8d418dfb9b3d4f=1536554669; uid=72477504203419866052170436187254212456480443827908674203911520518835128243063748574988921743732159011220945498651755943279106928; Hm_lpvt_4a001c429a59102d2d8d418dfb9b3d4f=1536569040'
    headers = {
        'Cookie': cookies,
    }
    request = urllib.request.Request(url=url, headers=headers)
    page = urllib.request.urlopen(request)  # 打开网页
    return page.read()  # 读取页面源码

def get_spider(url, list):
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find('ul', {'class': 'lefts'})
    tyleList = []
    for a in ul.children:
        # 类别链接
        try:
            if a != '\n':
                link = a['href']
                li = a.find('li')
                name = li.text
                tyleList.append({
                    'name': name,
                    'link': link
                })
        except BaseException as e:
            print (e)
    return tyleList

def get_category():
    records = []
    # url = 'http://127.0.0.1:5500/html/home.html'
    url = 'https://yx.5kjr.cn'
    # url = 'https://yx.5kjr.cn/pchome/index/getSubType'
    params = [
        {'type': '西药', 'id': '26'},
        {'type': '进口药品', 'id': '27'},
        {'type': '中药饮片', 'id': '60'},
        {'type': '医疗器械', 'id': '61'},
        {'type': '非药品', 'id': '63'},
        {'type': '保健食品', 'id': '64'},
        {'type': '其他类', 'id': '65'},
        {'type': '中成药', 'id': '75'},
        {'type': '注射药品', 'id': '301'},
    ]
    # post_category(url, params)
    return get_spider(url, records)
    # return records
    # write_csv(records)
    # print len(records)
    # print records

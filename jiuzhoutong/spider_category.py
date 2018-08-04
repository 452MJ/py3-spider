# coding:utf-8

import pandas as pd
from bs4 import BeautifulSoup
import urllib


def get_html(url):
    page = urllib.request.urlopen(url)  # 打开网页
    return page.read()  # 读取页面源码


def write_csv(list):
    columns = ['一级分类', '二级分类', '链接']
    csvfile = pd.DataFrame(columns=columns, data=list)  # 打开方式还可以使用file对象
    csvfile.to_csv('云药库分类.csv', index=False, encoding='GBK')


def get_spider(url, list):
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find('ul', {'class': 'mc'})
    for i in ul.children:
        # 药品名
        try:
            if i != '\n':
                div_category = i.find('div',{'class':'category'})
                h3 = div_category.find('h3')
                category_1 = h3.text # 一级分类
                dl_array = div_category.findAll('dl')
                for i2 in dl_array:
                    category_2 = i2.dt.a.text
                    a = i2.dt.a
                    href = a['href']
                    list.append([category_1, category_2, href])
                    # for i3 in i2.dd:
                    #     if i3 != '\n':
                    #         category_3 = i3.find('a').text
                    #         list.append([category_1,category_2,category_3])
        except BaseException as e:
            print (e)


def get_category():
    records = []
    # url = 'http://127.0.0.1:5500/html/home.html'
    url = 'http://www.xty999.com/'
    get_spider(url, records)
    return records
    # write_csv(records)
    # print len(records)
    # print records

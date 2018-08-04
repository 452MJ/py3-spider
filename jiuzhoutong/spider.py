# coding:utf-8
# encoding=utf8

import pandas as pd
from bs4 import BeautifulSoup
import urllib
from urllib.parse import quote


def get_html_nologin(url):
    page = urllib.request.urlopen(url)  # 打开网页
    return page.read()  # 读取页面源码


def get_html(url):
    cookies = 'pgv_pvi=3535526912; _qddaz=QD.6v9xrp.wvt1r1.jjr5nsj0; tencentSig=9099254784; ProductHistory_2_110495=110495; Hm_lvt_4b7dccaf26f8031679c7b9406fae960a=1532613562,1532613584,1532613631,1532701391; IESESSION=alive; pgv_si=s1316931584; JSESSIONID=5B919FC09D96865F232F90A6F4958C9A; _qddamta_800103661=3-0; _qdda=3-1.31jji7; _qddab=3-n5j03p.jk69e192; _qddac=3-2-1.31jji7.n5j03p.jk69e192; Hm_lpvt_4b7dccaf26f8031679c7b9406fae960a=1532833619'
    headers = {
        # 'GET': url + ' HTTP/1.1',
        # 'Host': 'www.xty999.com',
        # 'Proxy-Connection': 'keep-alive',
        # 'Upgrade-Insecure-Requests': '1',
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36 QQBrowser/4.4.105.400',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Referer': 'http://www.xty999.com/index.html',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cookie': cookies,
    }
    request = urllib.request.Request(url=url, headers=headers)
    page = urllib.request.urlopen(request)  # 打开网页
    return page.read()  # 读取页面源码


def write_csv(list):
    columns = ['分类', '药品名', '产品规格', '生产厂家', '零售参考价', '采购价']
    csvfile = pd.DataFrame(columns=columns, data=list)  # 打开方式还可以使用file对象
    csvfile.to_csv('九州通.csv', index=False, encoding='GBK')


def get_total_page(url):
    html = get_html_nologin(url)
    # html = get_html('http://127.0.0.1:5500/html/index.html')
    soup = BeautifulSoup(html, "html.parser")
    span = soup.find('span', {'class': 'pagination-info'})
    return span.text[2:][:-1]


def get_spider(url, list, category):
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find('ul', {'class': 'm_search_lst f_cbli'})
    for i in ul.children:
        dic = [category, '药品名', '产品规格', '生产厂家', '零售参考价', '采购价']
        # 药品名
        try:
            if i != '\n':
                # 药品名
                a = i.find('a', {'class': 'u_goods_tit'})
                a_text = a.text
                a_text = a_text.split( )
                dic[1] = a_text[1]
                dic[2] = a_text[2][1:]
                # 生产厂家
                p = i.find('p', {'class': 'u_goods_com'})
                dic[3] = p['title']
                # 零售价
                span_suprice = i.find('span', {'class': 'u_goods_field u_goods_suprice'})
                if span_suprice != None:
                    dic[4] = span_suprice.text
                else:
                    dic[4] = ''
                # 采购价
                span_price = i.find('span', {'class': 'u_goods_pric'})
                dic[5] = span_price.text
                list.append(dic)
        except BaseException as e:
            print(page + e)

records = []
category_array = [
    '感冒清热药物',
    '营养保健品',
    '外用药物',
    '心脑血管药物',
    '消化系统药物',
    '中药材/中药饮片',
    '补益安神药物',
    '其它商品',
]
for category_index in range(len(category_array)):
    # if category_index != 7:
    #     continue
    category = category_array[category_index]
    url = 'http://fds.yyjzt.com/search/merchandise.htm?classifyName=' + quote(category)
    total = get_total_page(url)
    total = int(total)
    for i in range(total):
        page = i + 1
        url = 'http://fds.yyjzt.com/search/merchandise.htm?classifyName=' + quote(category) + '&page=' + str(page)
        get_spider(url, records, category)
        print('{0}/{1} {2}/{3}'.format(category_index + 1, len(category_array), page, total))
write_csv(records)

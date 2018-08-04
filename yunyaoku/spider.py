# coding:utf-8

import pandas as pd
from bs4 import BeautifulSoup
import urllib

from yunyaoku.spider_category import get_category


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
        'Cookie': cookies,
    }
    request = urllib.request.Request(url=url, headers=headers)
    page = urllib.request.urlopen(request)  # 打开网页
    return page.read()  # 读取页面源码


def write_csv(list):
    columns = ['一级分类', '二级分类', '药品名', '产品规格', '生产厂家', '零售参考价', '采购价']
    csvfile = pd.DataFrame(columns=columns, data=list)  # 打开方式还可以使用file对象
    csvfile.to_csv('云药库.csv', index=False, encoding='GBK')


def get_total_page(url):
    html = get_html_nologin(url)
    # html = get_html('http://127.0.0.1:5500/html/index.html')
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find('div', {'class': 's-pager'})
    if div is None:
        return 0
    span_array = div.findAll('span')
    span = span_array[1].text
    span = span[1:len(span)]
    span = span[:-1]
    return span


def get_spider(url, list, category):
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find('ul', {'class': 'itemlist'})
    for i in ul.children:
        dic = [category[0], category[1]]
        # 药品名
        try:
            if i != '\n':
                # 药品名
                h3 = i.find('h3')
                dic.append(h3.a.text)
                ##
                ul_array = i.findAll('ul')
                if ul_array[0].text == '\n':
                    del ul_array[0];
                li = ul_array[0].findAll('li')
                # 产品规格
                if len(li) >= 4:
                    dic.append(li[3].text[5:])
                else:
                    dic.append('')
                # 生产厂家
                if len(li) >= 3:
                    dic.append(li[2].text[5:])
                else:
                    dic.append('')
                # 零售价
                li = ul_array[2].findAll('li')
                dic.append(li[1].text[7:])
                # 采购价
                span = ul_array[3].find('span', {'class': 'info'})
                if span is not None:
                    dic.append(span.text)
                else:
                    dic.append('')
                list.append(dic)
        except BaseException as e:
            print(page + e)


category_array = get_category()
records = []
for category_index in range(len(category_array)):
    # if category_index > 1:
    #     continue
    category = category_array[category_index]
    # category = category_array[123]
    href = category[2]
    url = 'http://www.xty999.com' + href
    total = get_total_page(url)
    total = int(total)
    for i in range(total):
        # time.sleep(1)
        page = i + 1
        url = 'http://www.xty999.com/productlist.ac?page=' + str(page)
        get_spider(url, records, category)
    print('{0}/{1}'.format(category_index + 1, len(category_array)))
write_csv(records)

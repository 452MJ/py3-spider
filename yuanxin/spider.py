# coding:utf-8

import pandas as pd
from bs4 import BeautifulSoup
import urllib

from yuanxin.spider_category import get_category
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def get_html(url):
    cookies = 'PHPSESSID=it3q07hcnjhc5rh22bo0545qo0; Hm_lvt_4a001c429a59102d2d8d418dfb9b3d4f=1536554669; uid=72477504203419866052170436187254212456480443827908674203911520518835128243063748574988921743732159011220945498651755943279106928; Hm_lpvt_4a001c429a59102d2d8d418dfb9b3d4f=1536569040'
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
    columns = ['药品分类', '商品名称', '包装规格', '生产厂家', '批准文号', '采购价', '折扣价', '销量']
    csvfile = pd.DataFrame(columns=columns, data=list)  # 打开方式还可以使用file对象
    csvfile.to_csv('源鑫.csv', index=False, encoding='GBK')


def get_total_page(url):
    html = get_html(url)
    # html = get_html('http://127.0.0.1:5500/html/index.html')
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find('ul', {'class': 'pagination'})
    li_array = ul.findAll('li')
    for i in range(len(li_array)):
        try:
            if i + 2 == len(li_array):
                a = li_array[i].find('a')
                total_page = a.text
                return total_page
        except BaseException as e:
            print(e)


def get_item_list(url, item_list, category):
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    div_array = soup.findAll('div', {'class': 'single_pro'})
    item_link_list = []
    sale_array = []
    for i in range(len(div_array)):
        try:
            a = div_array[i].find('a')
            item_link = a['href']
            item_link_list.append(item_link)
            span = div_array[i].find('span', {'class': 'sales'})
            if (span != None):
                span = span.text
                span = span[2:len(span)]
                span = span[:-1]
                sale_array.append(span)
            else:
                sale_array.append(0)
        except BaseException as e:
            print(e)
    for i in range(len(item_link_list)):
        try:
            item_list.append(get_item_detail('https://yx.5kjr.cn' + item_link_list[i], category, sale_array[i]))
        except BaseException as e:
            print(e)
    return item_list


def get_item_detail(url, category, sale):
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    # 采购价
    refer_span = soup.find('span', {'class': 'refer_price_one'})
    refer_price = refer_span.text
    # 折扣价
    activity_span = soup.find('span', {'class': 'activity_price_one'})
    activity_price = activity_span.text
    # 商品名称 包装规格 生产厂家 批准文号
    tbody = soup.find('table')
    tr_array = tbody.findAll('tr')
    # 商品名称
    item_name = tr_array[0].findAll('td')
    item_name = item_name[1].text
    # 包装规格
    item_standard = tr_array[1].findAll('td')
    item_standard = item_standard[1].text
    # 生产厂家
    item_supplier = tr_array[2].findAll('td')
    item_supplier = item_supplier[1].text
    # 批准文号
    item_number = tr_array[3].findAll('td')
    item_number = item_number[1].text
    return [
        category['name'],
        item_name,
        item_standard,
        item_supplier,
        item_number,
        refer_price,
        activity_price,
        sale
    ]
    # return {
    #     'category': category,
    #     'refer_price': refer_price,
    #     'activity_price': activity_price,
    #     'item_name': item_name,
    #     'item_standard': item_standard,
    #     'item_supplier': item_supplier,
    #     'item_number': item_number,
    # }


category_array = get_category()
records = []
for category_index in range(len(category_array)):
    # if category_index > 1:
    #     continue
    category = category_array[category_index]
    link = category['link']
    url = 'https://yx.5kjr.cn' + link
    total = get_total_page(url)
    total = int(total)
    for i in range(total):
        # time.sleep(1)
        page = i + 1
        final_url = url + '?page=' + str(page)
        get_item_list(final_url, records, category)
        print((category_index + 1), '/', len(category_array), '  ', (i + 1), "/", total)
write_csv(records)

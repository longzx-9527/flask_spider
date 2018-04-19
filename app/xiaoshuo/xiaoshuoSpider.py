# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-03-10 21:41:55
# @cnblog:http://www.cnblogs.com/lonelyhiker/

import requests
import sys
from bs4 import BeautifulSoup
from pymysql.err import ProgrammingError
from app.xiaoshuo.spider_tools import get_one_page, insert_fiction, insert_fiction_content, insert_fiction_lst
from app.models import Fiction_Lst, Fiction_Content, Fiction


def search_fiction(name, flag=1):
    """输入小说名字

    返回小说在网站的具体网址
    """
    if name is None:
        raise Exception('小说名字必须输入！！！')

    url = 'http://zhannei.baidu.com/cse/search?s=920895234054625192&q={}'.format(
        name)

    html = get_one_page(url, sflag=flag)
    soup = BeautifulSoup(html, 'html5lib')
    result_list = soup.find('div', 'result-list')
    fiction_lst = result_list.find_all('a', 'result-game-item-title-link')
    fiction_url = fiction_lst[0].get('href')
    fiction_name = fiction_lst[0].text.strip()
    fiction_img = soup.find('img')['src']
    fiction_comment = soup.find_all('p', 'result-game-item-desc')[0].text
    fiction_author = soup.find_all(
        'div', 'result-game-item-info')[0].find_all('span')[1].text.strip()

    if fiction_name is None:
        print('{} 小说不存在！！！'.format(name))
        raise Exception('{} 小说不存在！！！'.format(name))

    fictions = (fiction_name, fiction_url, fiction_img, fiction_author,
                fiction_comment)
    save_fiction_url(fictions)

    return fiction_name, fiction_url


def get_fiction_list(fiction_name, fiction_url, flag=1):
    # 获取小说列表
    fiction_html = get_one_page(fiction_url, sflag=flag)
    soup = BeautifulSoup(fiction_html, 'html5lib')
    dd_lst = soup.find_all('dd')
    fiction_lst = []
    fiction_url_tmp = fiction_url.split('/')[-2]
    for item in dd_lst[12:]:
        fiction_lst_name = item.a.text.strip()
        fiction_lst_url = item.a['href'].split('/')[-1].strip('.html')
        fiction_real_url = fiction_url + fiction_lst_url + '.html'
        lst = (fiction_name, fiction_url_tmp, fiction_lst_url,
               fiction_lst_name, fiction_real_url)
        fiction_lst.append(lst)
    return fiction_lst


def get_fiction_content(fiction_url, flag=1):
    fiction_id = fiction_url.split('/')[-2]
    fiction_conntenturl = fiction_url.split('/')[-1].strip('.html')
    fc = Fiction_Content().query.filter_by(
        fiction_id=fiction_id, fiction_url=fiction_url).first()
    if fc is None:
        print('此章节不存在，需下载')
        html = get_one_page(fiction_url, sflag=flag)
        soup = BeautifulSoup(html, 'html5lib')
        content = soup.find(id='content')
        f_content = str(content)
        save_fiction_content(fiction_url, f_content)
    else:
        print('此章节已存在，无需下载！！！')


def save_fiction_url(fictions):
    args = (fictions[0], fictions[1].split('/')[-2], fictions[1], fictions[2],
            fictions[3], fictions[4])
    insert_fiction(*args)


def save_fiction_lst(fiction_lst):
    total = len(fiction_lst)
    if Fiction().query.filter_by(fiction_id=fiction_lst[0][1]) == total:
        print('此小说已存在！！，无需下载')
        return 1
    for item in fiction_lst:
        print('此章节列表不存在，需下载')
        insert_fiction_lst(*item)


def save_fiction_content(fiction_url, fiction_content):
    fiction_id = fiction_url.split('/')[-2]
    fiction_conntenturl = fiction_url.split('/')[-1].strip('.html')
    insert_fiction_content(fiction_conntenturl, fiction_content, fiction_id)


def down_fiction_lst(f_name):
    # 1.搜索小说
    args = search_fiction(f_name, flag=0)
    # 2.获取小说目录列表
    fiction_lst = get_fiction_list(*args, flag=0)
    # 3.保存小说目录列表
    flag = save_fiction_lst(fiction_lst)
    print('下载小说列表完成！！')


def down_fiction_content(f_url):
    get_fiction_content(f_url, flag=0)
    print('下载章节完成！！')

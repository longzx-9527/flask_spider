# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-04-16 21:41:55
# @cnblog:http://www.cnblogs.com/lonelyhiker/

import requests
import sys
from bs4 import BeautifulSoup
from pymysql.err import ProgrammingError
from .spider_tools import (get_one_page, insert_many, insert_one,
                           select_fiction_many, select_fiction_one)


def search_fiction(name):
    """输入小说名字

    返回小说在网站的具体网址
    """
    if name is None:
        raise Exception('小说名字必须输入！！！')

    url = 'http://zhannei.baidu.com/cse/search?s=920895234054625192&q={}'.format(
        name)
    html = get_one_page(url)
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


def get_fiction_list(fiction_name, fiction_url):
    # 获取小说列表
    fiction_html = get_one_page(fiction_url)
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


def get_fiction_contents(fiction_lst):
    iCnt = 0
    total = len(fiction_lst)
    for fiction in fiction_lst:
        iCnt += 1
        sel_sql = "select count(*) from fiction_content where  fiction_id = '{}' and fiction_url= '{}'".format(
            fiction[1], fiction[2])
        if select_fiction_one(sel_sql)[1][0] > 0:
            print('此章节[{}]已下载！！！'.format(fiction[3]))
            continue
        get_fiction_content(fiction[-1])
        percent = float(iCnt) * 100 / float(total)
        sys.stdout.write("%.4f" % percent)
        sys.stdout.write("%\r")
        sys.stdout.flush()
    sys.stdout.write("100%!finish!\r")
    sys.stdout.flush()


def get_fiction_content(fiction_url):
    html = get_one_page(fiction_url)
    soup = BeautifulSoup(html, 'html5lib')
    content = soup.find(id='content')
    save_fiction_content(fiction_url, content)


def save_fiction_url(fictions):
    sql = """insert into fiction(fiction_name,fiction_id,fiction_real_url,fiction_img,fiction_author,fiction_comment)
    VALUES('%s','%s','%s','%s','%s','%s')"""
    args = (fictions[0], fictions[1].split('/')[-2], fictions[1], fictions[2],
            fictions[3], fictions[4])
    sel_sql = "select * from fiction where fiction_id = '{}'".format(args[1])
    if select_fiction_one(sel_sql)[0] == 0:
        insert_one(sql, args)


def save_fiction_lst(fiction_lst):
    total = len(fiction_lst)
    sel_sql = "select count(*) from fiction_lst where  fiction_id= '{}'".format(
        fiction_lst[0][1])

    if select_fiction_one(sel_sql)[1][0] == total:
        print('此小说已存在！！，无需下载')
        return 1

    for item in fiction_lst:
        sql = "insert into fiction_lst(fiction_name,fiction_id,fiction_lst_url,fiction_lst_name,fiction_real_url)values('%s','%s','%s','%s','%s')"
        sel_sql = "select count(*) from fiction_lst where fiction_lst_url = '{}' and fiction_id= '{}'".format(
            item[2], item[1])

        if select_fiction_one(sel_sql)[1][0] == 0:
            insert_one(sql, item)


def save_fiction_content(fiction_url, fiction_content):
    sql = """
        insert into fiction_content(fiction_id,fiction_url,fiction_content)values('%s','%s','%s')
        """
    fiction_id = fiction_url.split('/')[-2]
    fiction_conntenturl = fiction_url.split('/')[-1].strip('.html')
    sel_sql = "select count(*) from fiction_content where fiction_url = '{}' and fiction_id='{}' ".format(
        fiction_conntenturl, fiction_id)
    if select_fiction_one(sel_sql)[1][0] == 0:
        try:
            insert_one(sql, (fiction_id, fiction_conntenturl, fiction_content))
        except ProgrammingError as p:
            print('这个章节[{}]有毒，不下载了！！'.format(fiction_conntenturl))
            print('error={}'.format(p))
            return


def down_fiction_lst(f_name):
    # 1.搜索小说
    args = search_fiction(f_name)

    # 2.获取小说目录列表
    fiction_lst = get_fiction_list(*args)
    # 3.保存小说目录列表
    flag = save_fiction_lst(fiction_lst)


def down_fiction_content(f_url):
    get_fiction_content(f_url)


def main(name):
    # 1.搜索小说
    args = search_fiction(name)

    # 2.获取小说目录列表
    fiction_lst = get_fiction_list(*args)

    # 3.保存小说目录列表
    flag = save_fiction_lst(fiction_lst)

    if flag == 1:
        print('小说已存在，无需更新！！')
        return
    else:
        # 3.1 获取每一章节内容
        get_fiction_contents(fiction_lst)
        print('下载完毕！！！')


if __name__ == '__main__':
    lst = ['圣墟', '剑来', '我从凡间来', '我是至尊', '飞剑问道', '龙王传说']
    for x in lst:
        main(x)

# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-03-08 20:56:26
"""
爬虫常用工具包
将一些通用的功能进行封装
"""
from functools import wraps
from random import choice, randint
from time import ctime, sleep, time

import pymysql
import requests
from requests.exceptions import RequestException
from app.models import Fiction, Fiction_Content, Fiction_Lst
from app import db

#请求头
headers = {}
headers[
    'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
headers['Accept-Encoding'] = 'gzip, deflate, br'
headers['Accept-Language'] = 'zh-CN,zh;q=0.9'
headers['Connection'] = 'keep-alive'
headers['Upgrade-Insecure-Requests'] = '1'

agents = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
]


def get_one_page(url, proxies=None, sflag=1):
    #获取给定的url页面
    while True:
        try:
            headers['User-Agent'] = choice(agents)
            # 控制爬取速度
            if sflag:
                print('放慢下载速度。。。。。。')
                sleep(randint(1, 3))

            print('正在下载:', url)
            if proxies:
                r = requests.get(
                    url, headers=headers, timeout=5, proxies=proxies)
            else:
                r = requests.get(url, headers=headers, timeout=5)

        except Exception as r:
            print('errorinfo:', r)
            continue
        else:
            if r.status_code == 200:
                r.encoding = r.apparent_encoding
                print('爬取成功！！！')
                return r.text
            else:
                continue


def insert_fiction(fiction_name, fiction_id, fiction_real_url, fiction_img,
                   fiction_author, fiction_comment):
    fiction = Fiction().query.filter_by(fiction_id=fiction_id).first()
    if fiction is None:
        fiction = Fiction(
            fiction_name=fiction_name,
            fiction_id=fiction_id,
            fiction_real_url=fiction_real_url,
            fiction_img=fiction_img,
            fiction_author=fiction_author,
            fiction_comment=fiction_comment)
        db.session.add(fiction)
        db.session.commit()
    else:
        print('记录已存在，无需下载')


def insert_fiction_lst(fiction_name, fiction_id, fiction_lst_url,
                       fiction_lst_name, fiction_real_url):
    fl = Fiction_Lst().query.filter_by(
        fiction_id=fiction_id, fiction_lst_url=fiction_lst_url).first()
    if fl is None:
        fl = Fiction_Lst(
            fiction_name=fiction_name,
            fiction_id=fiction_id,
            fiction_lst_url=fiction_lst_url,
            fiction_lst_name=fiction_lst_name,
            fiction_real_url=fiction_real_url)
        db.session.add(fl)
        db.session.commit()
    else:
        print('此章节已存在！！！')


def insert_fiction_content(fiction_url, fiction_content, fiction_id):
    fc = Fiction_Content(
        fiction_id=fiction_id,
        fiction_content=fiction_content,
        fiction_url=fiction_url)
    db.session.add(fc)
    db.session.commit()

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


def get_one_page(url, proxies=None):
    #获取给定的url页面
    while True:
        try:
            headers['User-Agent'] = choice(agents)
            # 控制爬取速度
            # sleep(randint(1, 3))
            print('正在下载:', url)
            if proxies:
                # r = requests.get(url, headers=headers, timeout=5, proxies=proxies)
                r = requests.get(url)
            else:
                r = requests.get(url, headers=headers, timeout=5)
        except RequestException as r:
            continue
        else:
            if r.status_code == 200:
                r.encoding = r.apparent_encoding
                return r.text
            else:
                continue


def get_db(host='localhost', user='lzx', passwd='123', database='blog'):
    try:
        db = pymysql.connect(
            host=host,
            user=user,
            password=passwd,
            database=database,
            charset='utf8')
    except pymysql.err.OperationalError as e:
        print('error:', e)
        raise Exception('connect db error')
    return db


def get_cursor(db, cursor=None):
    if cursor:
        return db.cursor(cursor=cursor)
    else:
        return db.cursor()


def sql_executemany(cur, sql, lst):
    # 对于插入多条操作
    return cur.executemany(sql, lst)


def insert_one(sql, args):
    sql = sql % args
    sql_execute(sql)


def insert_many(sql, args):
    db = get_db()
    cursor = get_cursor(db)
    cursor.executemany(sql, args)
    db.commit()
    cursor.close()
    db.close()


def select_fiction_one(sql):
    db = get_db()
    with db.cursor() as cursor:
        cnt = cursor.execute(sql)
        lst = cursor.fetchone()
    db.close()
    return cnt, lst


def select_fiction_many(sql):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql)
        lst = cursor.fetchall()
    db.close()
    return lst


def sql_execute(sql):
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute(sql)
            db.commit()
    except Exception as e:
        print('sql=', sql)
        raise Exception('db error')
    finally:
        db.close()

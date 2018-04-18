# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-03-22 21:08:54

import os
from time import strftime

# 用于存放数据
BASE_PATH = os.path.join(os.getcwd(), 'data')
# 日志文件
LOG_FILE = os.path.join(BASE_PATH, 'xiaoshuo.log')
# 用于存放爬取状态，可用于断点爬取
LOG_STAT = os.path.join(BASE_PATH, 'spider_state.json')
# 豆瓣电影分类文件
MOVIES_TYPE_FILE = os.path.join(BASE_PATH, 'movies_type.csv')

# 豆瓣电影网页
main_url = 'https://movie.douban.com/chart'
# 用于获取电影列表信息
baseurl = 'https://movie.douban.com/j/chart/'
# 获取豆瓣电影json数据类型
top_list_type = ['top_list_count?', 'top_list?']
# 电影加载数
MOVIE_LIMIT = 20

# 日志文件
LOG_DIR = os.path.join(BASE_PATH, 'log')
LOGGER_FILE = os.path.join(LOG_DIR, 'info_{}.log'.format(strftime('%Y%m%d')))
LOGGER_ERROR_FILE = os.path.join(LOG_DIR, 'error_{}.log'.format(
    strftime('%Y%m%d')))

if not os.path.exists(BASE_PATH):
    os.mkdir(BASE_PATH)

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-04-15 08:53:34
# @cnblog:http://www.cnblogs.com/lonelyhiker/
import os
from time import strftime
import logging

log_name = os.path.join(
    os.getenv('HOME'), 'log/flask/log_{}.log'.format(strftime('%Y%m%d')))

FLASK_LOG_FILE = os.getenv('FLASK_LOG_FILE') or log_name

if not os.path.exists(os.path.dirname(FLASK_LOG_FILE)):
    os.makedirs(os.path.dirname(FLASK_LOG_FILE))


def init_logger(verbose=1, log_name=None):
    # 1.获取日志器
    logger = logging.getLogger(log_name)
    # 设置日志级别
    logger.setLevel(logging.DEBUG if verbose > 1 else logging.INFO)

    # 2.获取处理器
    f_handler = logging.FileHandler(FLASK_LOG_FILE, encoding='utf-8')
    formatter = logging.Formatter(
        '[%(asctime)s %(filename)s:%(lineno)s] - %(message)s')
    f_handler.setFormatter(formatter)
    f_handler.setLevel(logging.DEBUG)

    # 3.将处理器添加到日志器中
    logger.addHandler(f_handler)

    return logger


logger = init_logger(log_name='flask')

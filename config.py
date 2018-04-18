# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-04-14 11:42:41
# @cnblog:http://www.cnblogs.com/lonelyhiker/

import os

from time import strftime
import logging

log_name = os.path.join(
    os.getenv('HOME'), 'log/flask/log_{}.log'.format(strftime('%Y%m%d')))

FLASK_LOG_FILE = os.getenv('FLASK_LOG_FILE') or log_name

if not os.path.exists(os.path.dirname(FLASK_LOG_FILE)):
    os.makedirs(os.path.dirname(FLASK_LOG_FILE))


def get_handler():

    # 获取处理器
    f_handler = logging.FileHandler(FLASK_LOG_FILE, encoding='utf-8')
    formatter = logging.Formatter(
        '[%(asctime)s %(filename)s:%(lineno)s] - %(message)s')
    f_handler.setFormatter(formatter)
    f_handler.setLevel(logging.DEBUG)

    return f_handler


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """默认配置 主要是对数据库进行相关配置
    对象关系映射（Object Relational Mapping，简称ORM）是通过使用描述对象和数据库之间映射的元数据，
    将面向对象语言程序中的对象自动持久化到关系数据库中。
    这样，我们在具体的操作业务对象的时候，就不需要再去和复杂的SQL语句打交道，只要像平时操作对象一样操作它就可以了。
　　ORM框架就是用于实现ORM技术的程序。

    SQLAlchemy是Python编程语言下的一款开源软件。提供了SQL工具包及对象关系映射（ORM）工具，使用MIT许可证发行。
    
    SQLAlchmey采用了类似于Java里Hibernate的数据映射模型，
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'can you guess it'
    DEBUG = True
    # sqlalchemy两个主要配置
    # ORM底层所访问数据库URI
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://lzx:123@192.168.66.188/blog'
    # 当关闭数据库是否自动提交事务
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 是否追踪修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        # app.logger.setLevel(logging.DEBUG)
        # app.logger.addHandler(get_handler)
        pass


class DevelopmentConfig(Config):
    """开发环境配置
    """

    #可以通过修改SQLALCHEMY_DATABASE_URI来控制访问不同数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://lzx:123@192.168.66.188/blog'


class TestConfig(Config):
    """测试环境配置
    """

    #可以通过修改SQLALCHEMY_DATABASE_URI来控制访问不同数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://lzx:123@192.168.66.188/blog'


class ProductionConfig(Config):
    """生产环境
    """
    #可以通过修改SQLALCHEMY_DATABASE_URI来控制访问不同数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://lzx:123@192.168.66.188/blog'


# 设置配置映射
config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'test': TestConfig,
    'default': DevelopmentConfig
}

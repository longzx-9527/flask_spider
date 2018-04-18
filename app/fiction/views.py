# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-03-20 20:45:37
# @cnblog:http://www.cnblogs.com/lonelyhiker/

from flask import render_template, request, redirect, url_for

from app.xiaoshuo.xiaoshuoSpider import down_fiction_lst, down_fiction_content

from . import fiction
from ..models import Fiction, Fiction_Content, Fiction_Lst
import requests
from bs4 import BeautifulSoup
from app import db


@fiction.route('/book/')
def book_index():
    fictions = Fiction().query.all()
    print(fictions)
    return render_template('fiction_index.html', fictions=fictions)


@fiction.route('/book/list/<f_id>')
def book_lst(f_id):
    fictions = Fiction().query.all()

    for fiction in fictions:
        if fiction.fiction_id == f_id:
            break
    print(fiction)
    fiction_lst = Fiction_Lst().query.filter_by(fiction_id=f_id).all()
    if len(fiction_lst) == 0:
        print(fiction.fiction_name)
        down_fiction_lst(fiction.fiction_name)
        return render_template('fiction_error.html', message='暂无此章节信息，请重新刷新下')

    fiction_name = fiction_lst[0].fiction_name
    return render_template(
        'fiction_lst.html',
        fictions=fictions,
        fiction=fiction,
        fiction_lst=fiction_lst,
        fiction_name=fiction_name)


@fiction.route('/book/fiction/')
def fiction_content():
    fic_id = request.args.get('id')
    f_url = request.args.get('f_url')
    print('获取书本 id={} url={}'.format(fic_id, f_url))

    # 获取上一章和下一章信息
    fiction_lst = Fiction_Lst().query.filter_by(
        fiction_id=fic_id, fiction_lst_url=f_url).first()
    id = fiction_lst.id
    fiction_name = fiction_lst.fiction_lst_name
    pre_id = id - 1
    next_id = id + 1
    fiction_pre = Fiction_Lst().query.filter_by(
        id=pre_id).first().fiction_lst_url
    fiction_next = Fiction_Lst().query.filter_by(
        id=next_id).first().fiction_lst_url
    f_id = fic_id
    # 获取具体章节内容
    fiction_contents = Fiction_Content().query.filter_by(
        fiction_id=fic_id, fiction_url=f_url).first()
    if fiction_contents is None:
        print('fiction_real_url={}'.format(fiction_lst.fiction_real_url))
        r = requests.get(fiction_lst.fiction_real_url)
        down_fiction_content(fiction_lst.fiction_real_url)
        print('fiction_id={} fiction_url={}'.format(fic_id, f_url))
        fiction_contents = Fiction_Content().query.filter_by(
            fiction_id=fic_id, fiction_url=f_url).first()
    if fiction_contents is None:
        return render_template('fiction_error.html', message='暂无此章节信息，请重新刷新下')
    print('fiction_contents=', fiction_contents)
    fiction_content = fiction_contents.fiction_content
    return render_template(
        'fiction.html',
        f_id=f_id,
        fiction_name=fiction_name,
        fiction_pre=fiction_pre,
        fiction_next=fiction_next,
        fiction_content=fiction_content)


@fiction.route('/book/search/')
def f_search():
    f_name = request.args.get('f_name')
    print('收到输入：', f_name)
    # 1.查询数据库存在记录
    fictions = Fiction().query.all()
    for x in fictions:
        if f_name in x.fiction_name:
            fiction = x
            break

    if fiction:
        fiction_lst = Fiction_Lst().query.filter_by(
            fiction_id=fiction.fiction_id).all()
        if fiction_lst is None:
            down_fiction_lst(f_name)
            fictions = Fiction().query.all()
            print('fictions=', fictions)
            for fiction in fictions:
                if f_name in fiction.fiction_name:
                    break

            if f_name not in fiction.fiction_name:
                return render_template('fiction_error.html', message='暂无此小说信息')

            fiction_lst = Fiction_Lst().query.filter_by(
                fiction_id=fiction.fiction_id).all()
            return render_template(
                'fiction_lst.html',
                fictions=fictions,
                fiction=fiction,
                fiction_lst=fiction_lst,
                fiction_name=fiction.fiction_name)
        else:
            fiction_name = fiction_lst[0].fiction_name
            return render_template(
                'fiction_lst.html',
                fictions=fictions,
                fiction=fiction,
                fiction_lst=fiction_lst,
                fiction_name=fiction_name)
    else:
        down_fiction_lst(f_name)
        fictions = Fiction().query.all()
        print('fictions=', fictions)
        for fiction in fictions:
            if f_name in fiction.fiction_name:
                break

        if f_name not in fiction.fiction_name:
            return render_template('fiction_error.html', message='暂无此小说信息')

        fiction_lst = Fiction_Lst().query.filter_by(
            fiction_id=fiction.fiction_id).all()
        return render_template(
            'fiction_lst.html',
            fictions=fictions,
            fiction=fiction,
            fiction_lst=fiction_lst,
            fiction_name=fiction.fiction_name)

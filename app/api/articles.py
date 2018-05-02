# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-04-24 18:03:29
# @cnblog:http://www.cnblogs.com/lonelyhiker/
import re
import markdown
from time import strftime
from flask_restful import Resource, reqparse, fields, marshal_with
from ..models import Article
from ..models import db
from ..tools import generate_id

post_parser = reqparse.RequestParser()

post_parser.add_argument(
    'article_title', type=str, required=True, help="article_title is required")
post_parser.add_argument('article_content', type=str, required=True)
post_parser.add_argument('f_type', type=str)
post_parser.add_argument('article_url', type=str)

# 格式化输出
resource_full_fields = {
    'article_id': fields.String,
    'article_title': fields.String,
    'article_text': fields.String,
    'article_summary': fields.String,
    'article_read_cnt': fields.Integer,
    'article_sc': fields.Integer,
    'article_pl': fields.Integer,
    'article_date': fields.DateTime,
    'article_url': fields.String,
    'article_type': fields.String,
    'article_author': fields.String,
    'user_id': fields.String
}


class Articles(Resource):
    @marshal_with(resource_full_fields)
    def get(self, article_id=None):
        if article_id:
            article = Article().query.filter_by(article_id=article_id).first()
            if article:
                return article
            else:
                return {"code": 200, "message": "article no exists"}
        else:
            return {"code": 404, "message": "article_id is none"}

    def post(self):
        post_args = post_parser.parse_args()
        article_title = post_args.get('article_title')
        artitle_type = post_args.get('f_type')
        article_text = post_args.get('article_content')
        article_url = post_args.get('article_url')
        article_text = markdown.markdown(article_text, ['extra', 'codehilite'])
        article_id = generate_id('article')
        article_date = strftime('%Y-%m-%d %H:%M:%S')
        article_type = '技术杂谈' if artitle_type == '1' else '人生感悟'
        content = re.compile('.*?>(.*?)<').findall(article_text)
        article_summary = ''
        for x in content:
            if x:
                article_summary = article_summary + x
                if len(article_summary) > 250:
                    break

        print('article_title=', article_title)
        print('article_type=', article_type)
        print('article_date=', article_date)
        article_summary = "".join(article_summary.split())
        print('article_summary=', article_summary)
        article = Article(
            article_id=article_id,
            article_title=article_title,
            article_type=article_type,
            article_text=article_text,
            article_summary=article_summary[:180],
            article_url=article_url,
            article_date=article_date,
            user_id=current_user.user_id,
            article_author=current_user.user_name)
        db.session.add(article)
        db.session.commit()
        print('add article finished')
        articles = Article().query.limit(8)
        return articles

    def delete(self, article_id=None):
        if article_id:
            article = Article().query.filter_by(article_id=article_id).first()
            db.session.delete(article)
            db.session.commit()
            return {"code": 200, "message": "delete success"}
        else:
            return {"code": 301, "message": "article_id error "}


class ArticleList(Resource):
    @marshal_with
    def get(self, user_id):
        if user_id:
            articles = Article().query.filter_by(user_id=user_id).all()
        else:
            articles = Article().query.order_by(article_id).all()
        return articles

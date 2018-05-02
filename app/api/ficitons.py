# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-04-24 18:03:29
# @cnblog:http://www.cnblogs.com/lonelyhiker/

from flask_restful import Resource, reqparse
from flask import Request
from ..models import Fiction, Fiction_Content, Fiction_Lst
from ..models import db

post_parser = reqparse.RequestParser()

post_parser.add_argument(
    'user_name', type=str, required=True, help="user_name is required")
post_parser.add_argument('nickname', type=str, required=True)
post_parser.add_argument('sex', type=str)
post_parser.add_argument('age', type=int)
post_parser.add_argument('password', type=str)
post_parser.add_argument('email', type=str, required=True)


class Users(Resource):
    print('user resource init')

    def get(self, user_id=None):
        pass

    def post(self):
        post_args = post_parser.parse_args()
        user = User.query.filter_by(user_name=post_args['user_name']).first()
        if user:
            return jsonify({"status": 0, "msg": "此用户已存在！！"})
        user = User(
            user_name=post_args['user_name'],
            nickname=post_args['nickname'],
            sex=post_args['sex'],
            password=post_args['password'],
            email=post_args['email'])
        db.session.add(user)
        db.session.commit()
        return jsonify()

    def put(self):
        pass

# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-04-24 18:03:29
# @cnblog:http://www.cnblogs.com/lonelyhiker/
from flask import jsonify
from flask_restful import Resource, fields, marshal_with, reqparse

from ..models import User, db
from ..tools import generate_id
from .authentication import auth
"""
parser = reqparse.RequestParser()
parser.add_argument(*args,**kwargs)
args = parser.parse_args()
args是获取传来值组成的字典

add_argument参数说明
type:传入要转换成的类型(int,str,float)
require:默认false，设置为True这个值必输
action:append获取多个值，如http://localhost/?name=1&name=2
dest:给传入参数key重命名
location:参数位置，从Request.json/Request.args/Request.form/Request.values,headers,user_agent
单个位置：location='args'
多个位置: location= ['args','form']

继承解析
parser_copy = parser.copy()

"""

post_parser = reqparse.RequestParser()

post_parser.add_argument(
    'user_name', type=str, required=True, help="user_name is required")
post_parser.add_argument('nickname', type=str, required=True)
post_parser.add_argument('sex', type=str)
post_parser.add_argument('age', type=int)
post_parser.add_argument('password', type=str)
post_parser.add_argument('email', type=str, required=True)

resource_users = {
    'user_id': fields.String,
    'user_name': fields.String,
    'nickname': fields.String,
    'sex': fields.String,
    'age': fields.String,
    'email': fields.String,
    'last_login_tm': fields.DateTime,
    'user_crt_dt': fields.DateTime,
    'attention_cnt': fields.Integer
}


class Users(Resource):
    @marshal_with(resource_users)
    def get(self, user_id=None):
        user = User().query.filter_by(user_id=user_id).first()
        return user

    def delete(self, user_id=None):
        user = User().query.filter_by(user_id=user_id).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"status": 200, "message": "delete success"})
        else:
            return jsonify({
                "status": 404,
                "message": "user_id is not exists delete fail"
            })


class UserList(Resource):
    @auth.login_required
    @marshal_with(resource_users)
    def get(self):
        users = User().query.all()
        return users

    def post(self):
        post_args = post_parser.parse_args()
        print("user_name:", post_args.get("user_name"))
        user = User.query.filter_by(user_name=post_args['user_name']).first()
        if user:
            return jsonify({"status": 200, "message": "此用户已存在！！"})
        else:
            user = User(
                user_name=post_args['user_name'],
                nickname=post_args['nickname'],
                sex=post_args['sex'],
                password=post_args['password'],
                email=post_args['email'])
            user.user_id = generate_id('user')
            db.session.add(user)
            db.session.commit()
            print('add user success')
            return jsonify({"status": 200, "message": "success"})

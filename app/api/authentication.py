# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-04-22 20:20:55
# @cnblog:http://www.cnblogs.com/lonelyhiker/

from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth

from . import auth_api
from ..models import User

auth = HTTPBasicAuth()


@auth_api.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.user_name})


@auth_api.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token})


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(user_name=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-03-19 23:44:05
# @cnblog:http://www.cnblogs.com/lonelyhiker/
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask import current_app

from . import db, login_manager


class Fiction(db.Model):
    __tablename__ = 'fiction'
    # __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    fiction_name = db.Column(db.String)
    fiction_id = db.Column(db.String)
    fiction_real_url = db.Column(db.String)
    fiction_img = db.Column(db.String)
    fiction_author = db.Column(db.String)
    fiction_comment = db.Column(db.String)
    update = db.Column(db.String)
    new_content = db.Column(db.String)
    new_url = db.Column(db.String)

    def __repr__(self):
        return '<fiction %r> ' % self.fiction_name


class Fiction_Lst(db.Model):
    __tablename__ = 'fiction_lst'
    # __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    fiction_name = db.Column(db.String(255))
    fiction_id = db.Column(db.String(255))
    fiction_lst_url = db.Column(db.String(255))
    fiction_lst_name = db.Column(db.String(255))
    fiction_real_url = db.Column(db.String(255))

    def __repr__(self):
        return '<fiction_lst %r> ' % self.fiction_name


class Fiction_Content(db.Model):
    __tablename__ = 'fiction_content'
    # __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    fiction_url = db.Column(db.String(255))
    fiction_content = db.Column(db.Text)
    fiction_id = db.Column(db.Integer)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.String(20), primary_key=True)
    user_name = db.Column(db.String(30), unique=True)
    nickname = db.Column(db.String(40), unique=True)
    sex = db.Column(db.String(4))
    age = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(50), unique=True)
    last_login_tm = db.Column(db.DateTime)
    user_crt_dt = db.Column(db.DateTime)
    attention_cnt = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<{},{},{}>'.format(self.user_name, self.email, self.user_id)

    # 增加密码属性
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # 设置密码
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 校验密码
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.user_id

    def generate_auth_token(self, expiration=3600):
        #生成令牌字符串token
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'user_id': self.user_id}).decode("utf-8")

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return None  # valid token, but expired
        return User.query.get(data['user_id'])


class Article(db.Model):
    __tablename__ = 'article'
    article_id = db.Column(db.String(20), primary_key=True)
    article_title = db.Column(db.String(100), nullable=False)
    article_text = db.Column(db.Text)
    article_summary = db.Column(db.String(255))
    article_read_cnt = db.Column(db.Integer, default=0)
    article_sc = db.Column(db.Integer, default=0)
    article_pl = db.Column(db.Integer, default=0)
    article_date = db.Column(db.DateTime)
    article_url = db.Column(db.Text)
    article_type = db.Column(db.String(10))
    article_author = db.Column(db.String(20))
    user_id = db.Column(db.String(20))


class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.String(20), primary_key=True)
    comment_text = db.Column(db.Text)
    comment_date = db.Column(db.DateTime)
    comment_name = db.Column(db.String(30))
    comment_support = db.Column(db.Integer, default=0)
    comment_oppose = db.Column(db.Integer, default=0)
    article_id = db.Column(db.String(20), nullable=False)


class Task(db.Model):
    __tablename__ = "task"
    task_id = db.Column(db.String(20), primary_key=True)
    task_name = db.Column(db.String(50), nullable=False)
    start_dt = db.Column(db.String(16))
    next_dt = db.Column(db.String(16))
    content = db.Column(db.String(200))
    stat = db.Column(db.String(10))
    remind = db.Column(db.String(10))
    article_id = db.Column(db.String(20))
    user_id = db.Column(db.String(20))
    emails = db.Column(db.String(200))
    stage = db.Column(db.Integer, default=1)


# 公共参数表
class Commparam(db.Model):
    __tablename__ = 'commparam'
    # 参数名称
    param_name = db.Column(db.String(10), primary_key=True)
    # 参数值1
    param_value = db.Column(db.Integer, default=1)
    # 参数值2
    param_text = db.Column(db.String(100))
    # 参数状态 0-正常 1-停用
    param_stat = db.Column(db.String(2), default='0')


# 加载用户的回调函数
@login_manager.user_loader
def load_user(user_id):
    print('call load_user')
    return User.query.get(user_id)

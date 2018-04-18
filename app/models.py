# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-03-19 23:44:05
# @cnblog:http://www.cnblogs.com/lonelyhiker/

from . import db


class Fiction(db.Model):
    __tablename__ = 'fiction'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    fiction_name = db.Column(db.String)
    fiction_id = db.Column(db.String)
    fiction_real_url = db.Column(db.String)
    fiction_img = db.Column(db.String)
    fiction_author = db.Column(db.String)
    fiction_comment = db.Column(db.String)

    def __repr__(self):
        return '<fiction %r> ' % self.fiction_name


class Fiction_Lst(db.Model):
    __tablename__ = 'fiction_lst'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    fiction_name = db.Column(db.String)
    fiction_id = db.Column(db.String)
    fiction_lst_url = db.Column(db.String)
    fiction_lst_name = db.Column(db.String)
    fiction_real_url = db.Column(db.String)

    def __repr__(self):
        return '<fiction_lst %r> ' % self.fiction_name


class Fiction_Content(db.Model):
    __tablename__ = 'fiction_content'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    fiction_url = db.Column(db.String)
    fiction_content = db.Column(db.String)
    fiction_id = db.Column(db.String)

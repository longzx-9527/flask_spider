# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-05-02 17:08:45
# @cnblog:http://www.cnblogs.com/lonelyhiker/

from flask import jsonify
from flask_restful import Resource, fields, reqparse, marshal_with
from ..models import Comment

comment_resource = {
    "comment_id": fields.String,
    "comment_text": fields.String,
    "comment_date": fields.DateTime,
    "comment_name": fields.String,
    "comment_support": fields.Integer,
    "comment_oppose": fields.Integer,
    "article_id": fields.String
}


class Comments(Resource):
    @marshal_with(comment_resource)
    def get(self, article_id=None):
        comments = Comment().query.filter_by(article_id=article_id).all()
        return comments

    def post(self, article_id=None):
        comment_name = request.form.get("name")
        commentary = request.form.get("commentary")
        commentary = markdown.markdown(commentary, ['extra', 'codehilite'])
        comment_id = generate_id('comment')
        comment_date = strftime('%Y-%m-%d %H:%M:%S')
        print('comment:', commentary)
        comment = Comment(
            comment_id=comment_id,
            comment_text=commentary,
            comment_date=comment_date,
            comment_name=comment_name,
            article_id=article_id)
        db.session.add(comment)
        db.session.commit()
        return jsonfiy({"status": "200", "message": "add success"})


class Commentsupport(Resource):
    @marshal_with(comment_resource)
    def put(self, comment_id=None):
        comment = Comment().query.filter_by(comment_id=comment_id).first()
        comment.comment_support += 1
        db.session.add(comment)
        db.session.commit()
        return comment


class Commentoppose(Resource):
    @marshal_with(comment_resource)
    def put(self, comment_id=None):
        comment = Comment().query.filter_by(comment_id=comment_id).first()
        comment.comment_oppose += 1
        db.session.add(comment)
        db.session.commit()
        return comment

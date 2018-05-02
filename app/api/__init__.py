# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-04-22 20:08:25
# @cnblog:http://www.cnblogs.com/lonelyhiker/

from flask import Blueprint
from flask_restful import Api

api = Api()
auth_api = Blueprint(name='auth_api', import_name=__name__)
from . import authentication

# 文章路由
from .articles import Articles, ArticleList

api.add_resource(Articles, "/api/articles", endpoint="get_articles")
api.add_resource(
    Articles, "/api/articles/<article_id>", endpoint="get_article")

api.add_resource(ArticleList, "/api/articlelist")
api.add_resource(
    ArticleList, "/api/articlelist/<user_id>", endpoint="articleList")

# 用户路由
from .users import Users, UserList
api.add_resource(Users, "/api/users/<user_id>")
api.add_resource(UserList, "/api/users")

# 评论路由
from .comments import Comments, Commentsupport, Commentoppose

api.add_resource(Comments, "/api/comments/<article_id>")
api.add_resource(Commentsupport, "/api/commentsp/<comment_id>")
api.add_resource(Commentoppose, "/api/commentop/<comment_id>")

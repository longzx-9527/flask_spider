import csv
from flask import render_template, url_for, redirect, request, make_response, current_app

from . import main
from .forms import LoginForm
from ..mylogger import logger
from app import pages
import requests
import markdown


@main.route('/')
def index(user=None):
    articles = list(pages._pages.values())
    print(articles)
    return render_template('index.html', articles=articles, user=user)


@main.route('/login_in/', methods=['POST', 'GET'])
def login_in():
    loginForm = LoginForm()
    logger.debug('用户登录')
    if loginForm.validate_on_submit():
        username = loginForm.username.data
        password = loginForm.password.data
        current_app.logger.debug('username=%s password=%s', username, password)
        return redirect(url_for('main.index'))
    return render_template('login.html', form=loginForm, action='/login_in/')


@main.route('/login_up/', methods=['GET', 'POST'])
def login_up():
    registerForm = RegisterForm()
    logger.debug('用户注册')
    if registerForm.validate_on_submit():
        username = registerForm.username.data
        email = registerForm.email.data
        current_app.logger.debug('username=%s email=%s', username, email)
        return redirect(url_for('main.index'))
    return render_template('login_up.html', form=registerForm)


@main.route('/article/<path:path>/')
def get_article(path):
    page = pages.get_or_404(path)
    with open('/home/longzx/src/study/flask/app/pages/我的文章.md') as f:
        content = f.read()
    content = markdown.markdown(content)
    return render_template('article.html', page=page, content=content)


@main.route('/wrarticle/', methods=['GET', 'POST'])
def wrarticle():
    if request.method == 'POST':
        artitle_title = request.form.get('title')
        artitle_type = request.form.get('f_type')
        artitle_content = request.form.get('article_content')
        print('article=', artitle_content)
        print('title', artitle_title)
        print('type=', artitle_type)
        artitle_content = markdown.markdown(artitle_content)
        print('article=', artitle_content)
        page = None
        return render_template(
            'article.html', page=page, content=artitle_content)
    else:
        return render_template('wrarticle.html')

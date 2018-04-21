import csv
import markdown
import requests
from time import strftime
from flask import (current_app, make_response, redirect, render_template,
                   request, url_for, flash)
from flask_login import login_required, current_user, login_user

from . import main
from app.models import User, Article, Comment, db
from ..mylogger import logger
from .forms import LoginForm, RegisterForm
from ..tools import generate_id


@main.route('/')
def index():
    articles = Article().query.all()
    print(articles)
    return render_template('index.html', articles=articles)


@main.route('/login_in/', methods=['POST', 'GET'])
def login_in():
    loginForm = LoginForm()
    logger.debug('用户登录')
    if loginForm.validate_on_submit():
        username = loginForm.username.data
        password = loginForm.password.data
        user = User.query.filter_by(user_name=username).first()
        if user is not None and user.verify_password(password):
            login_user(user, remember=loginForm.remember_me.data)
            return redirect(url_for('main.index'))
    return render_template('login.html', form=loginForm, action='/login_in/')


@main.route('/login_up/', methods=['GET', 'POST'])
def login_up():
    registerForm = RegisterForm()
    logger.debug('用户注册')
    if registerForm.validate_on_submit():
        username = registerForm.username.data
        user = User.query.filter_by(user_name=username).first()
        if user:
            flask('用户名已存在')
        email = registerForm.email.data
        passwd1 = registerForm.password.data
        passwd2 = registerForm.password2.data
        if passwd1 != passwd2:
            flash('两次密码不一致，请从新输入！')

        user = User(user_name=username, email=email, password=passwd1)
        user.user_id = generate_id('user')
        print('user=', user)
        db.session.add(user)
        db.session.commit()
        print('注册成功')
        return redirect(url_for('main.login_in'))
    return render_template('login_up.html', form=registerForm)


@main.route('/login_out')
@login_required
def login_out():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@main.route('/get_article/<article_id>/')
def get_article(article_id):
    article = Article().query.filter_by(article_id=article_id).first()
    articles = Article().query.limit(8)
    return render_template('article.html', article=article, articles=articles)


@main.route('/wrarticle/', methods=['GET', 'POST'])
@login_required
def wrarticle():
    if request.method == 'POST':
        print(request.form)
        article_title = request.form.get('article_title')
        artitle_type = request.form.get('f_type')
        article_text = request.form.get('article_content')
        article_url = request.form.get('article_url')
        article_text = markdown.markdown(article_text, ['extra', 'codehilite'])

        article_id = generate_id('article')
        article_date = strftime('%Y-%m-%d %H:%M:%S')
        article_type = '技术杂谈' if artitle_type == '1' else '人生感悟'
        print('article_title=', article_title)
        print('article_type=', article_type)
        print('article_date=', article_date)
        article = Article(
            article_id=article_id,
            article_title=article_title,
            article_type=article_type,
            article_text=article_text,
            article_url=article_url,
            article_date=article_date,
            user_id=current_user.user_id,
            article_author=current_user.user_name)
        db.session.add(article)
        db.session.commit()
        print('add article finished')
        articles = Article().query.limit(8)
        return render_template(
            'article.html', article=article, articles=articles)
    else:
        return render_template('wrarticle.html')

import re
import markdown
import requests
from time import strftime
from flask import (current_app, make_response, redirect, render_template,
                   request, url_for, flash)
from flask_login import login_required, current_user, login_user, logout_user

from . import main
from ..models import User, Article, Comment, db
from ..mylogger import logger
from .forms import LoginForm, RegisterForm
from ..tools import generate_id


@main.route('/')
def index():
    logger.info('index')
    articles = Article().query.all()
    print(articles)
    return render_template('index.html', articles=articles, flag=1)


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
    article.article_read_cnt = article.article_read_cnt + 1
    db.session.add(article)
    db.session.commit()
    articles = Article().query.limit(8)
    comments = Comment().query.filter_by(article_id=article_id).all()
    return render_template(
        'article.html', article=article, articles=articles, comments=comments)


@main.route('/wrarticle/', methods=['GET', 'POST'])
@login_required
def wrarticle():
    if request.method == 'POST':
        article_title = request.form.get('article_title')
        artitle_type = request.form.get('f_type')
        article_text = request.form.get('article_content')
        article_url = request.form.get('article_url')
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
        return render_template(
            'article.html', article=article, articles=articles)
    else:
        return render_template('wrarticle.html')


@main.route('/wrcomment/<article_id>', methods=["POST"])
def wrcomment(article_id):
    print('article_id:', article_id)
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
    return redirect(url_for("main.get_article", article_id=article_id))


@main.route('/comment_oppose/<comment_id>')
def comment_oppose(comment_id):
    comment = Comment().query.filter_by(comment_id=comment_id).first()
    comment.comment_oppose += 1
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("main.get_article", article_id=comment.article_id))


@main.route('/comment_support/<comment_id>')
def comment_support(comment_id):
    print('comment_id:', comment_id)
    comment = Comment().query.filter_by(comment_id=comment_id).first()
    comment.comment_support += 1
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("main.get_article", article_id=comment.article_id))


@main.route('/del_article/<article_id>/')
@login_required
def del_article(article_id):
    print('article_id=', article_id)
    article = Article().query.filter_by(article_id=article_id).first()
    db.session.delete(article)
    db.session.commit()
    print('删除文章成功!!!!')
    return redirect(url_for('main.manage_article'))


@main.route('/manage_article/')
@login_required
def manage_article():
    articles = Article().query.filter_by(user_id=current_user.user_id).all()
    return render_template('manage_article.html', articles=articles)


@main.route('/technology/')
def get_technology():
    articles = Article().query.filter_by(article_type='技术杂谈').all()
    return render_template('index.html', articles=articles, flag=2)


@main.route('/life/')
def get_life():
    articles = Article().query.filter_by(article_type='人生感悟').all()
    return render_template('index.html', articles=articles, flag=3)

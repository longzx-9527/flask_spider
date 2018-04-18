import csv
from flask import render_template, url_for, redirect, request, make_response, current_app

from . import main
from .forms import LoginForm
from ..mylogger import logger
import requests


@main.route('/')
def index():
    movie_lst = []
    current_app.logger.debug('hello in index')
    articles = [{
        'title': '这会光is东方杰无法',
    }]

    return render_template('index.html', articles=articles)


@main.route('/login_in/', methods=['POST', 'GET'])
def login_in():
    loginForm = LoginForm()
    logger.debug('用户登录')
    if loginForm.validate_on_submit():
        username = loginForm.username.data
        email = loginForm.email.data
        current_app.logger.debug('username=%s email=%s', username, email)
        return redirect(url_for('main.index'))
    return render_template('login.html', form=loginForm, action='/login_in/')


@main.route('/login_up/', methods=['GET', 'POST'])
def login_up():
    loginForm = LoginForm()
    logger.debug('用户注册')
    if loginForm.validate_on_submit():
        username = loginForm.username.data
        email = loginForm.email.data
        current_app.logger.debug('username=%s email=%s', username, email)
        return redirect(url_for('main.index'))
    return render_template('login.html', form=loginForm)

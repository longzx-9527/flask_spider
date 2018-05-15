# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-05-11 22:31:54
# @cnblog:http://www.cnblogs.com/lonelyhiker/

import os
import contextlib
import configparser
import smtplib
import pymysql
from datetime import timedelta, datetime
from email.header import Header
from email.mime.text import MIMEText
"""
发送定时任务,到指定邮箱
"""
cf = configparser.ConfigParser()
cf.read('/home/longzx/etc/config.ini')
print(cf.sections())


def sendEmail(content=None, title=None, receivers=None):
    mail_host = cf.get('MAIL', 'mail_host')
    mail_user = cf.get('MAIL', 'mail_user')
    mail_pass = cf.get('MAIL', 'mail_pass')
    sender = mail_user
    print('user={} pass={}'.format(mail_user, mail_pass))
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)
        for i in range(len(title)):
            message = MIMEText(content[i], 'html', 'utf-8')  # 内容, 格式, 编码
            message['From'] = "{}".format(sender)
            message['To'] = ",".join(receivers)
            message['Subject'] = title[i]
            smtpObj.sendmail(sender, receivers, message.as_string())

        smtpObj.close()
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)


def get_next_dt(begin_dt=None, stage=1):
    print(begin_dt)
    if stage == 1:
        return begin_dt + timedelta(days=1)
    if stage == 2:
        return begin_dt + timedelta(days=2)
    if stage == 3:
        return begin_dt + timedelta(days=4)
    if stage == 4:
        return begin_dt + timedelta(days=7)
    if stage == 5:
        return begin_dt + timedelta(day=14)
    return False


#定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(
        host=cf.get("DATABASE", 'host'),
        port=cf.getint('DATABASE', 'port'),
        user=cf.get('DATABASE', 'user'),
        passwd=cf.get('DATABASE', 'passwd'),
        db=cf.get('DATABASE', 'db'),
        charset=cf.get('DATABASE', 'charset')):
    conn = pymysql.connect(
        host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    with mysql() as cursor:
        now_dt = datetime.now().date()
        cnt = cursor.execute(
            "select * from task where next_dt =%s or remind='1' ", str(now_dt))
        results = cursor.fetchall()
        content = []
        title = []
        for task in results:
            next_dt = datetime.strptime(task.get('next_dt'), '%Y-%m-%d')
            if task.get('remind') == '1':
                content.append(task.get('content'))
                title.append(task.get('task_name'))
            elif now_dt == next_dt.date():
                next_dt = get_next_dt(next_dt, stage=task.get('stage') + 1)
                print('next_dt', next_dt)
                if next_dt == False:
                    continue
                else:
                    next_dt = str(next_dt.date())
                cursor.execute(
                    "update task set next_dt='%s',stage=%d where task_id='%s' "
                    % (next_dt, task.get('stage') + 1, task.get('task_id')))
                content.append(task.get('content'))
                title.append(task.get('task_name'))

        if cnt > 0:
            receivers = ['904185259@qq.com', 'longzongxing@dingtalk.com']
            sendEmail(content, title, receivers)

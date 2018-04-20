# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-04-10 18:02:22

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, TextField, DateField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, email
"""
字段类型      说　　明
StringField 文本字段
TextAreaField 多行文本字段
PasswordField 密码文本字段
HiddenField 隐藏文本字段
DateField 文本字段，值为 datetime.date 格式
DateTimeField 文本字段，值为 datetime.datetime 格式
IntegerField 文本字段，值为整数
DecimalField 文本字段，值为 decimal.Decimal
FloatField 文本字段，值为浮点数
BooleanField 复选框，值为 True 和 False
RadioField 一组单选框
SelectField 下拉列表
SelectMultipleField 下拉列表，可选择多个值
FileField 文件上传字段
SubmitField 表单提交按钮
FormField 把表单作为字段嵌入另一个表单
FieldList 一组指定类型的字段

验证函数 说　　明
Email 验证电子邮件地址
EqualTo 比较两个字段的值；常用于要求输入两次密码进行确认的情况
IPAddress 验证 IPv4 网络地址
Length 验证输入字符串的长度
NumberRange 验证输入的值在数字范围内
Optional 无输入值时跳过其他验证函数
Required 确保字段中有数据
Regexp 使用正则表达式验证输入值
URL 验证 URL
AnyOf 确保输入值在可选值列表中
NoneOf 确保输入值不在可选值列表中
"""


class LoginForm(FlaskForm):
    username = StringField(
        label='用户昵称',
        validators=[
            DataRequired("昵称必填"),
            Length(min=6, max=20, message="用户名必须介于6-20个字符")
        ],
        render_kw={"placeholder": "用户名必须介于6-20个字符"})
    password = PasswordField(
        label="用户密码",
        validators=[DataRequired("密码必填！")],
        render_kw={
            "placeholder": '密码必须大于6个字符',
        })

    remember_me = BooleanField(label='remember_me', default=False)
    submit = SubmitField(label='登录')


class RegisterForm(FlaskForm):
    username = StringField(
        label='用户昵称',
        validators=[
            DataRequired("昵称必填"),
            Length(min=6, max=20, message="用户名必须介于6-20个字符")
        ],
        render_kw={"placeholder": "用户名必须介于6-20个字符"})
    password = PasswordField(
        label="用户密码",
        validators=[DataRequired("密码必填！")],
        render_kw={
            "placeholder": '密码必须大于6个字符',
        })
    password2 = PasswordField(
        label="用户密码",
        validators=[DataRequired("密码必填！")],
        render_kw={
            "placeholder": '再次输入',
        })
    email = StringField(
        '邮箱',
        validators=[email(message="邮箱格式不正确！")],
        render_kw={"placeholder": "E-mail: yourname@example.com"})
    birthdate = DateField(
        label='日期',
        validators=[DataRequired('日期格式不正确')],
        render_kw={"placeholder": "日期如：2018-01-01"})
    submit = SubmitField(label='注册')

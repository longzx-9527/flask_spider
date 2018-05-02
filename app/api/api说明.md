# flask_spider的API说明

## 1.基于Token的认证及实现

    整体思路：
    1.用户使用用户名密码验证成功，返回token
    2.以后就是用token作为这个用户的通行证

## 1.1 修改modes.py

```python

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(UserMixin, db.Model):
    # ...

    def generate_auth_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expries_in=expiration)
        return s.dumps({'user_id': self.user_id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except expression as identifier:
            return None
        return User.query.get(data['user_id'])

```

## 1.2.authentication.py

验证客户信息：
1.实现verify_password回调函数去验证用户名和密码，验证通过返回True，否则返回False。
2.Flask-HTTPAuth再调用这个回调函数。

```python

from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth

from . import auth_api
from ..models import User

auth = HTTPBasicAuth()


@auth_api.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.user_name})


@auth_api.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token})


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(user_name=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

```

## 1.3 测试

```python
# 1.获取所有客户信息
$>curl  -i -X GET http://127.0.0.1:5000/api/users
HTTP/1.0 401 UNAUTHORIZED
Content-Type: text/html; charset=utf-8
Content-Length: 19
WWW-Authenticate: Basic realm="Authentication Required"
Server: Werkzeug/0.14.1 Python/3.6.1
Date: Wed, 02 May 2018 11:01:25 GMT
#提示需要认证

# 2.使用curl测试请求获取一个认证token
$>curl -u test:1234 -i -X GET http://127.0.0.1:5000/api/token
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 169
Server: Werkzeug/0.14.1 Python/3.6.1
Date: Wed, 02 May 2018 11:16:34 GMT

{
  "token": "eyJhbGciOiJIUzI1NiIsImlhdCI6MTUyNTI1OTc5NCwiZXhwIjoxNTI1MjYzMzk0fQ.eyJ1c2VyX2lkIjoiMjAxODA1MDIwMDAwMDAwMyJ9.4gS1ISMTw2yNH9ywCX8DWdHAR1BBMxB1QTdvlooDhNA"
}

# 3.使用token一访问受保护的API
$>curl -u eyJhbGciOiJIUzI1NiIsImlhdCI6MTUyNTI1ODMwOSwiZXhwIjoxNTI1MjYxOTA5fQ.eyJ1c2VyX2lkIjoiMjAxODA1MDIwMDAwMDAwMyJ9.JHDl4Ti8Ev_H9JMbHRnH8Le3PXfEh_5PGmMl3pAWNwQ:unused -i -X GET http://127.0.0.1:5000/api/users

[ {
        "user_id": "2018042100000002",
        "user_name": "Nicolas Cage",
        "nickname": null,
        "sex": null,
        "age": null,
        "email": "Nicolas Cage@163.com",
        "last_login_tm": null,
        "user_crt_dt": null,
        "attention_cnt": 0
    },
    {
        "user_id": "2018050200000003",
        "user_name": "test",
        "nickname": "test",
        "sex": null,
        "age": null,
        "email": "123@qq.com",
        "last_login_tm": null,
        "user_crt_dt": null,
        "attention_cnt": 0
    }
]
#请求里面带了unused字段。只是为了标识而已，替代密码的占位符。

```

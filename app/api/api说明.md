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

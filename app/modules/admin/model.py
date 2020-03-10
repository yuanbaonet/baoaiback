"""dao

Data Access Object

PROJECT: BaoAI Backend
AUTHOR: henry <703264459@qq.com>
WEBSITE: http://www.baoai.co
COPYRIGHT: Copyright © 2016-2020 广州源宝网络有限公司 Guangzhou Yuanbao Network Co., Ltd. ( http://www.ybao.org )
LICENSE: Apache-2.0
"""
import time
from app import db
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
# serializer for JWT
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# exceptions for JWT
from itsdangerous import SignatureExpired, BadSignature, BadData
from app.common.mixin import * 
from app.common.result import Result
from app.common.status import Status 

class Admin(TableMixin, db.Model):
    __tablename__ = 'admin'
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    nickname = db.Column(db.String(32))
    last_login_time = db.Column(db.DateTime)  # last login time
    last_login_ip = db.Column(db.String(32), nullable=True)  # last login ip
    current_login_ip = db.Column(db.String(32), nullable=True)  # current login IP
    current_login_time = db.Column(db.DateTime)  # current login time
    login_failure = db.Column(db.Integer, nullable=False, default=0) # login failure count
    avatar = db.Column(db.String(255), nullable=True) # avatar url
    locked = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return '<Admin %r>' % self.username

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verify Password # 验证密码
        """
        return check_password_hash(self.password_hash, password)

    def generate_token(self, expires=3600):
        """Generate Token # 产生令牌

        token contains id, username and timestamp
        令牌包含：id, username, 时间截

        """
        s = Serializer(
            secret_key=current_app.config['SECRET_KEY'],
            salt=current_app.config['AUTH_SALT'],
            expires_in=expires
        )
        timestamp = time.time()
        # token contains id, username and timestamp
        token = s.dumps({
            'id': self.id,
            'username': self.username,
            'iat': timestamp
        }).decode()
        return token

    def generate_new_token(self, expires, username, rftoken):
        """Generate new token with reflesh token # 使用刷新令牌获取新令牌

        Args:
            expires (int): expires time (unit: second)
            username (str): username
            rftoken (str): reflesh token
            
        Returns:
            str: new token, default is None

        """
        token = None
        res = Admin.confirm(rftoken)
        if res['status'] != Status.TOKEN_SUCCESS.status :
            return token
        if res['data']['username'] != username :
            return token
        s = Serializer(
            secret_key=current_app.config['SECRET_KEY'],
            salt=current_app.config['AUTH_SALT'],
            expires_in=expires
        )
        timestamp = time.time()
        # token contains id, username and timestamp
        token = s.dumps({
            'id': self.id,
            'username': self.username,
            'iat': timestamp
        }).decode()
        return token

    @staticmethod
    def confirm(token):
        """Confirm token # 确认令牌，返回确认状态

        Args:
            token (str): To be verified token
            
        Returns:
            object: app.common.result.Result 

        """
        # token decoding
        s = Serializer(
            secret_key=current_app.config['SECRET_KEY'],
            salt=current_app.config['AUTH_SALT'])
        data = {}
        try:
            data = s.loads(token)
            # token decoding faild
            # if it happend a plenty of times, there might be someone
            # trying to attact your server, so it should be a warning.
        except SignatureExpired:
            msg = 'token expired'
            # current_app.logger.warning(msg)
            return Result.error(data,status=Status.TOKEN_SIGNATURE_EXPIRED.status, message=Status.TOKEN_SIGNATURE_EXPIRED.message)
        except BadSignature as e:
            encoded_payload = e.payload
            if encoded_payload is not None:
                try:
                    s.load_payload(encoded_payload)
                except BadData:
                    # the token is tampered.
                    msg = 'token tampered'
                    return Result.error(data,status=Status.TOKEN_TAMPERED.status, message=Status.TOKEN_TAMPERED.message)
            msg = 'badSignature of token'
            return Result.error(data,status=Status.TOKEN_BADSIGNATURE.status, message=Status.TOKEN_BADSIGNATURE.message)
        except:
            msg = 'wrong token with unknown reason'
            return Result.error(data,status=Status.TOKEN_UNKNOWN_REASON.status, message=Status.TOKEN_UNKNOWN_REASON.message)
        if ('id' not in data) :
            msg = 'illegal payload inside'
            return Result.error(data,status=Status.TOKEN_ILLEGAL.status, message=Status.TOKEN_ILLEGAL.message)
        return Result.success(data=data,status=Status.TOKEN_SUCCESS.status, message=Status.TOKEN_SUCCESS.message)







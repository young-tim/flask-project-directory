# -*-coding:utf-8-*-
import datetime
from uuid import uuid1
import jwt
import time
from flask import current_app, request
from apps.app import db
from apps.models.user import UserModel, UserJwtLoginTimeModel
from apps.configs.site_config import SITE_CONFIG


class JwtAuth():

    '''
    JWT用户验证
    '''

    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id: <id>
        :param login_time: int(timestamp)
        :return: string
        """
        iat = datetime.datetime.utcnow()
        exp = iat + datetime.timedelta(days=0, seconds=SITE_CONFIG["rest_auth_token"]["LOGIN_LIFETIME"])

        try:
            payload = {
                'exp': exp,
                'iat': iat,
                'iss': SITE_CONFIG['site_info']['SITE_URL'],
                'data': {
                    'id': user_id,
                    'login_time': login_time,
                    'cid':str(uuid1())
                }
            }
            return {"token":jwt.encode(payload, current_app.secret_key,algorithm='HS256'),
                    "cid":payload["data"]["cid"]}
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, current_app.secret_key, leeway=SITE_CONFIG["rest_auth_token"]["LOGIN_LIFETIME"])
            #payload = jwt.decode(auth_token, get_config("key", "SECRET_KEY"), options={'verify_exp': True})
            if ('data' in payload and 'id' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError

        except jwt.ExpiredSignatureError:

            return 'BearerToken已过期'

        except jwt.InvalidTokenError:
            return 'BearerToken无效'

    def get_login_token(self, user):

        """
        用户登录成功后调用此函数,记录登录并获取token
        :param user:
        :return: json
        """
        now_time = time.time()
        result = self.encode_auth_token(user.id, now_time)

        # 查看当前jwt验证的登录客户端数
        jwt_login_time = user.jwt_login_time_dict
        if jwt_login_time:
            keys = jwt_login_time.keys()
            # 当jwt登录数大于等于配置限制时
            if len(keys) >= SITE_CONFIG['rest_auth_token']['MAX_SAME_TIME_LOGIN']:
                earliest = 0
                earliest_cid = None
                for k, v in jwt_login_time.items():
                    if v < earliest or earliest == 0:
                        earliest = v
                        earliest_cid = k
                if earliest_cid:
                    # 删除最早登录的jwt
                    tem_jwt_login_time = UserJwtLoginTimeModel.query\
                        .filter(UserJwtLoginTimeModel.id == earliest_cid)\
                        .order_by(UserJwtLoginTimeModel.login_time.asc())\
                        .first()
                    db.session.delete(tem_jwt_login_time)
                    db.session.commit()

                    del jwt_login_time[earliest_cid]

        # 添加新的jwt
        new_jwt_login_time = UserJwtLoginTimeModel(id = result["cid"],
                                                   login_time = round(now_time * 1000000))
        new_jwt_login_time.user = user

        db.session.add(new_jwt_login_time)
        db.session.commit()

        return result["token"].decode()


    def user_identify(self):
        """
        用户鉴权
        :return: (status, )
        """
        auth_token = request.headers.get('BearerToken')
        if auth_token:
            payload = self.decode_auth_token(auth_token)
            if not isinstance(payload, str):
                user = UserModel.query.get(payload['data']['id'])
                if not user:
                    result = (None, "用户身份验证失败，用户不存在")
                else:
                    if user.jwt_login_time_dict and payload['data']["cid"] in user.jwt_login_time_dict and \
                                    user.jwt_login_time_dict[payload['data']["cid"]] == payload['data']['login_time']:
                        result = (True, user)
                    else:
                        result = (None, '用户身份验证令牌已过期或已更改。请重新登录')
            else:
                result = (None, "令牌异常")
        else:
            result = (None, '未提供"BearerToken"用户身份验证令牌')
        return result


    def clean_login(self):
        """
        清理用户登录
        :return:
        """
        auth_token = request.headers.get('BearerToken')
        if auth_token:
            payload = self.decode_auth_token(auth_token)
            if not isinstance(payload, str):
                user = UserModel.query.get(payload['data']['id'])
                if not user:
                    result = (None, "用户身份验证失败，用户不存在")
                else:
                    if payload['data']["cid"] in user.jwt_login_time_dict and \
                                    user.jwt_login_time_dict[payload['data']["cid"]] == payload['data']['login_time']:

                        # 清除退出当前客户端的登录时间信息
                        jwt = UserJwtLoginTimeModel.query.filter(UserJwtLoginTimeModel.id == payload['data']["cid"], UserJwtLoginTimeModel.user_id == user.id).first()

                        db.session.delete(jwt)
                        db.session.commit()

                        result = (True, "")
                    else:
                        result = (True, "")
            else:
                result = (None, payload)
        else:
            result = (None, '未提供"BearerToken"用户身份验证令牌')
        return result
# -*-coding:utf-8-*-
import base64
from random import randint
from uuid import uuid1
import time
from flask import current_app, request
from werkzeug.exceptions import Unauthorized
from apps.app import db, cache, rest_session, weblog
from apps.configs.config import REST_SECRET_TOKEN_CACHE_KEY, REST_SECRET_TOKEN_CACHE_TIMEOUT
from apps.configs.site_config import SITE_CONFIG
from apps.core.flask.restful import succcess, unauthorized
from apps.models.sys import SysTokenModel
from apps.utils.format.obj_format import ormobj_to_dict


class RestTokenAuth():

    '''
    客户端验证
    '''

    @staticmethod
    def encode_auth_token():
        """
        生成认证Token
        id:str
        :return: string
        """
        id = "{}{}".format(str(uuid1()), randint(0, 999999))
        return {"token": base64.b64encode(id.encode()).decode()}

    '''
    SecretToken
    '''
    def create_secret_token(self):

        """
        管理端创建secret token
        """

        tokens = SysTokenModel.query.filter(SysTokenModel.token_type=='secret_token').all()
        if len(tokens) < 2:
            result = self.encode_auth_token()

            token = SysTokenModel(token_type="secret_token",
                                 key= result["token"],
                                 token= result["token"],
                                 is_active= 1,
                                 time= time.time())
            try:
                db.session.add(token)
                db.session.commit()

                cache.delete(REST_SECRET_TOKEN_CACHE_KEY)
                return True, ormobj_to_dict(token)
            except Exception as e:
                weblog.error(e)
                return False, "创建token失败"
        return False, "最多创建2个token"

    def activate_secret_token(self, token_id):

        """
        激活secret token
        :return:
        """

        r = SysTokenModel.query.filter_by(id=token_id).first()
        r.is_active = 1
        try:
            db.session.commit()

            cache.delete(REST_SECRET_TOKEN_CACHE_KEY)
            return True, "成功激活token"
        except Exception as e:
            weblog.error(e)
            return False, "token激活失败"

    def disable_secret_token(self, token_id):

        """
        停用secret token
        :return:
        """
        tokens = SysTokenModel.query.filter(SysTokenModel.token_type=="secret_token", SysTokenModel.is_active==1).all()
        if len(tokens) > 1:
            r = SysTokenModel.query.filter_by(id=token_id).first()
            r.is_active = 0

            try:
                db.session.commit(r)

                cache.delete(REST_SECRET_TOKEN_CACHE_KEY)
                return True, "成功禁用token"
            except Exception as e:
                weblog.error(e)
                return False, "token禁用失败"

        else:
            return False, "请至少保留一个token"

    def delete_secret_token(self, token_id):

        """
        删除token, 至少保留一个token
        :return:
        """

        tokens = SysTokenModel.query.filter(SysTokenModel.token_type == "secret_token").all()
        if len(tokens) > 1:
            token = SysTokenModel.query.filter_by(id=token_id).first()

            try:
                db.session.delete(token)
                db.session.commit()

                cache.delete(REST_SECRET_TOKEN_CACHE_KEY)
                return True, "成功删除token"
            except Exception as e:
                weblog.error(e)
                return False, "token删除失败"

        else:
            return False, "删除失败，请至少保留一个token"


    @property
    @cache.cached(key=REST_SECRET_TOKEN_CACHE_KEY, timeout=REST_SECRET_TOKEN_CACHE_TIMEOUT)
    def get_secret_tokens(self):
        tokens = SysTokenModel.query.filter_by(token_type='secret_token').all()

        token_info = []
        if not len(tokens):
            s,r = self.create_secret_token()
            token_info = [r]

        is_active_token = []
        for token in tokens:
            token_info.append(ormobj_to_dict(token))
            if token.is_active:
                is_active_token.append(token.token)

        data = {"token_info":token_info, "is_active_token":is_active_token}
        return data


    def auth_rest_token(self):
        auth_token_type = None
        auth_header = request.headers.get('RestToken')
        if auth_header:
            # 使用RestToken验证
            is_malformed = False
            auth_header = auth_header.split(" ")
            if len(auth_header) >= 2:
                if auth_header[0] == "SecretToken":
                    auth_token_type = "secret_token"
                    # 使用的是SecretToken, 固定Token
                    if not auth_header[1] in self.get_secret_tokens["is_active_token"]:
                        # SecretToken无效
                        response = current_app.make_response("RestsToken的SecretToken无效")
                        raise SecretTokenError(response.get_data(as_text=True), response=response)

                elif auth_header[0] == "AccessToken":
                    auth_token_type = "access_token"
                    self.auth_access_token(auth_header[1])
                else:
                    # 格式不对
                    is_malformed = True
            else:
                is_malformed = True
            if is_malformed:
                response = current_app.make_response("令牌格式不正确，应为 'SecretToken <token>'"
                                                             " 或 'AccessToken <token>' and 'ClientId <client_id>'")
                raise SecretTokenError(response.get_data(as_text=True), response=response)
        else:
            response = current_app.make_response(
                '令牌丢失，非网页浏览请求请提供"RestToken"，否则提供"X-CSRFToken"')
            raise TokenError(response.get_data(as_text=True), response=response)

        return auth_token_type


    '''
    Client Token
    '''

    def create_access_token(self):

        """
        创建client token, 用于rest api常用验证
        """
        r = self.auth_rest_token()
        if r == "secret_token":
            client_token = {"token":self.encode_auth_token()["token"],
                            "expiration":time.time()+SITE_CONFIG["rest_auth_token"]["REST_ACCESS_TOKEN_LIFETIME"]}
            sid = rest_session.set("access_token", client_token)
            if sid:
                data = {"client_id":sid, "access_token":client_token["token"]}
                return succcess(data)
            else:
                msg = "获取失败，请重试"
                return unauthorized(msg)
        else:
            msg: "请求头（request header）提供的RestToken不是SecretToken"
            return unauthorized(msg)


    def auth_access_token(self, token):

        '''
        验证client id 与client token
        :return:
        '''
        se_token = rest_session.get("access_token")
        if se_token:

            if se_token["token"] != token or se_token["expiration"]<=time.time():
                # 验证失败或者已过期
                response = current_app.make_response("AccessToken无效或已过期")
                raise AccessTokenError(response.get_data(as_text=True), response=response)
        else:

            # 找不到相关token
            response = current_app.make_response("找不到与'AccessToken'匹配的'ClientId'")
            raise AccessTokenError(response.get_data(as_text=True), response=response)

class SecretTokenError(Unauthorized):
    """
    错误请求类： SecretToken错误
    """
    description = 'RestToken中的SecretToken无效'

class AccessTokenError(Unauthorized):
    """
    错误请求类： AccessToken错误
    """
    description = 'RestToken中的AccessToken无效'

class TokenError(Unauthorized):
    """
    错误请求类： CSRFToken或者AccessToken未提供或者异常
    """
    description = 'RestToken验证失败'
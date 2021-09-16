# -*-coding:utf-8-*-
from flask import request
from flask_login import current_user
from apps.core.blueprint import api
from apps.core.flask.response import response_format


@api.route('/currentUserInfo', methods=['get'])
def api_current_user_info():
    '''
    GET:
        获取当前登录的用户信息
        :return:
    '''
    data = {}
    if current_user.is_authenticated:
        user_info = current_user.user_info

        data["is_authenticated"] = True
        data["user_info"] = user_info
    else:
        data["is_authenticated"] = False
        data["user_info"] = {}
    return response_format(data)

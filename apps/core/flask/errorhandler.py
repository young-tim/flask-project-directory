# -*-coding:utf-8-*-
import os
from flask import request, render_template, g
from flask_wtf.csrf import CSRFError
from werkzeug.utils import redirect

# from apps.configs.config import DEFAULT_ADMIN_LOGIN_PAGE
from apps.configs.site_config import SITE_CONFIG
from apps.core.auth.rest_token_auth import TokenError, SecretTokenError, AccessTokenError
from apps.core.blueprint import api #, admin
from apps.core.flask.login_manager import LoginReqError
from apps.core.flask.restful import notFound
from apps.core.flask.response import response_format
from apps.core.template.template import render_absolute_path_template
from apps.views.global_data.process.global_data import get_global_site_data


class ErrorHandler():

    '''
    配置各种异常状态返回数据 http status
    '''
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):

        @app.errorhandler(401)
        def internal_server_error_401(e):
            return internal_server_error(e)

        @app.errorhandler(404)
        def internal_server_error_404(e):
            return internal_server_error(e)

        @app.errorhandler(500)
        def internal_server_error_500(e):
            return internal_server_error(e)

        @app.errorhandler(SecretTokenError)
        def handle_rest_token_error(e):
            data = {"code": e.code, "msg": e.description, "error_id":40101}
            return response_format(data)

        @app.errorhandler(AccessTokenError)
        def handle_rest_token_error(e):
            data = {"code": e.code, "msg": e.description, "error_id": 40102}
            return response_format(data)

        @app.errorhandler(CSRFError)
        def handle_csrf_error(e):
            data = {"code": e.code, "msg": e.description, "error_id": 40103}
            return response_format(data)

        @app.errorhandler(TokenError)
        def handle_token_error(e):
            data = {"code": e.code, "msg": e.description, "error_id":40104,
                    "help":"Please add the 'RestToken' or 'X-CSRFToken' request header"}
            return response_format(data)

        @app.errorhandler(LoginReqError)
        def handle_login_error(e):
            data = {"code": e.code, "msg": e.description, "error_id": 40105,
                    "to_url":SITE_CONFIG["login_manager"]["LOGIN_VIEW"]}
            if request.headers.get('RestToken'):
                data["to_url"] = SITE_CONFIG["login_manager"]["LOGIN_VIEW"]

            if request.path.startswith(api.url_prefix):
                # api 响应Json数据
                return response_format(data)
            # 页面, 跳转到登录
            if request.path.startswith("/admin"):
                # return redirect(DEFAULT_ADMIN_LOGIN_PAGE)
                return redirect(data["to_url"])
            else:
                return redirect(data["to_url"])

def internal_server_error(e):
    '''
    处理服务器错误
    :param e:
    :return:
    '''
    try:
        code = e.code
    except:
        code = 500
    msg = "An error occurred. Please contact the administrator"
    if code == 401:
        msg = "Permission denied"

    elif code == 404:
        msg = "API不存在或已弃用"

    elif code == 500:
        msg = "Server error"

    elif isinstance(code, int) and code//500 == 1:
        msg = "Server error, please check whether the third-party plug-in is normal"

    data = {"code": code, "request_id": g.weblog_id,
            "msg": msg}
    if request.path.startswith(api.url_prefix):
        return response_format(data)
    else:
        g.site_global = dict(g.site_global, **get_global_site_data(req_type="view"))
        # path = "{}/pages/{}.html".format(get_config("theme", "CURRENT_THEME_NAME"), code)
        # absolute_path = os.path.abspath("{}/{}".format(theme_view.template_folder, path))
        # if not os.path.isfile(absolute_path):
        #     # 主题不存在<e.code>错误页面(如404页面),使用系统自带的页面
        #     path = "{}/module/exception/{}.html".format(admin.template_folder, code)
        #     return render_absolute_path_template(path, data=data), 404
        #
        # return render_template(path, data=data), code

		# TODO: 应该返回对应错误的页面（如上面注释内容）
        msg = "页面不存在"
        return response_format(notFound(msg))

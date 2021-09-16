from apps.app import csrf
from flask_wtf.csrf import generate_csrf
from apps.core.auth.rest_token_auth import TokenError
from apps.core.blueprint import api
from flask import request, g, current_app
from apps.views.token.process.rest_token import rest_token_auth
from apps.configs.config import API_TOKEN_ENABLED, FRONT_CSRF_ENABLED


class Request():

    def all(self, key, default_value=None):
        '''
        所有参数
        :param key: key
        :param d_value: None
        :return:
        '''
        if key in request.values:
            value = request.values[key]
        elif key in request.form:
            value = request.form[key]
        elif request.json and key in request.json:
            value = request.json[key]
        elif key in request.files:
            value = request.files[key]

            # 处理上传ppt/pptx文件时，文件名自动有"结尾的问题
            if '.ppt"' in value.filename or '.pptx"' in value.filename:
                value.filename = value.filename[:-1]
        else:
            value = default_value
        # 避免参数为空，且默认值不为空的取值错误
        if value == "" and value != default_value:
            value = default_value
        return value

    def list(self, key, default_value=None):
        '''
        列表
        :param key: key
        :param d_value: None
        :return:
        '''
        if key in request.values:
            value = request.values.getlist(key)
        elif key in request.form:
            value = request.form.getlist(key)
        elif request.json and key in request.json:
            value = request.json[key]
        elif key in request.files:
            value = request.files.getlist(key)

            # 处理上传ppt/pptx文件时，文件名自动有"结尾的问题
            if '.ppt"' in value.filename or '.pptx"' in value.filename:
                value.filename = value.filename[:-1]
        else:
            value = default_value
        return value


class RequestProcess():

    '''
    请求处理类
    '''
    def __init__(self, **kwargs):
        pass

    def init_request_process(self, app, **kwargs):
        @app.after_request
        def after_request_func(response):
            if FRONT_CSRF_ENABLED:
                # 调用函数生成 csrf_token
                csrf_token = generate_csrf()
                # 通过 cookie 将值传给前端
                response.set_cookie("csrf_token", csrf_token)

            return response

        @app.before_request
        def before_request_func():
            '''
            请求前执行函数
            :return:
            '''
            request.c_method = request.method
            if API_TOKEN_ENABLED and request.path.startswith(api.url_prefix):
                # 只要是api请求都需要token验证
                """
                token验证使用方式
                1.SecretToken与AccessToken用于在无CsrfToken时调用API请求的一个客户端令牌, 以验证客户端是否为伪造的. 而SecretToken是长期可用验证令牌(除非你停用或者删除了它), 需要保存在客户端使用.
                2.使用令牌时, 可以使用SecretToken做令牌或者ClientId与AccessToken组合做令牌(见使用方式).
                3.为了减少SecretToken的暴露风险, Restful api发送请求时, 尽量使用ClientId和AccessToken作为客户端验证令牌.
                4.当没有获取过AccessToken或者AccessToken失效时, 请通过/api/token/access-token获取新的AccessToken(具体请查看/api/token/access-token文档).
                这个时候只能使用SecretToken作为客户端令牌验证.
                5.使用SecretToken时, 尽量使用https
                使用方式:
                    在http请求中设置请求头
                    RestToken:"SecretToken xxxxxxx"
                    或
                    RestToken:"AccessToken xxxxxxx" 和 ClientId:"xxxxxxx"
              """
                auth_header = request.headers.get('RestToken')
                csrf_header = request.headers.get('X-CSRFToken')
                if csrf_header:
                    # 使用CSRF验证
                    csrf.protect()
                elif auth_header:
                    rest_token_auth.auth_rest_token()
                else:
                    response = current_app.make_response(
                        '令牌丢失，非网页浏览请求请提供"RestToken"，否则提供"X-CSRFToken"')

                    raise TokenError(response.get_data(as_text=True), response=response)

            request.argget = Request()

            '''
            兼容前端某些js框架或浏览器不能使用DELETE, PUT, PATCH等请求时,
            可以在参数中使用_method'
            '''
            if request.argget.all("_method"):
                request.c_method = request.argget.all("_method").upper()
            if not "site_global" in g:
                g.site_global = {}


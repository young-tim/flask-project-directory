# -*-coding:utf-8-*-
from flask import request
from flask_login import logout_user
from apps.core.auth.jwt_auth import JwtAuth
from apps.core.blueprint import api
from apps.core.flask.response import response_format
from apps.views.user.process.sign import sign_up, sign_in
from apps.configs.site_config import SITE_CONFIG
from apps.utils.format.obj_format import ormobj_to_dict, str_to_num


@api.route('/sign-up', methods=['POST'])
def api_sign_up():

    '''
    POST:
        1.普通用户使用邮箱注册
        emial:<emial>, 邮箱
        username: <str>, 用户名
        password: <str>,密码
        password2: <str>,再次确认密码
        code:<str>, 邮箱收取到的code


        2.普通用户使用手机注册
        phone:<int>手机号码
        username: <str>, 用户名
        password: <str>,密码
        password2: <str>,再次确认密码
        code:<str>, 手机收取到的code

        :return:
    '''
    data = sign_up()
    return response_format(data)


@api.route('/sign-in', methods=['PUT'])
def api_sign_in():
    '''
    PUT:
        1.普通登录
        username: <str>, 用户名或邮箱或手机号码
        password: <str>,密码
        remember_me:<int>,是否记住登录，0 不记住，1 记住登录
        next:<str>, 登录后要返回的to url, 如果为空,则返回设置中的LOGIN_TO
        use_jwt_auth:<int>, 是否使用jwt验证. 0 或 1,默认为0不使用

        当多次输入错误密码时，api会返回open_img_verif_code:true,
        表示需要图片验证码验证,客户端应该请求验证码/api/vercode/image,
         然后后再次提交登录时带下如下参数
        再次提交登录时需要以下两个参数
        code:<str>, 图片验证码中的字符
        code_url_obj:<json>,图片验证码url 对象
        :return:
    '''

    data = sign_in()
    return response_format(data)


@api.route('/sign-out',  methods=['GET', 'PUT'])
def sign_out():

    '''
    GET or PUT:
        用户登出api
        use_jwt_auth:<int>, 是否使用jwt验证. 0 或 1,默认为0不使用.
                     如果是jwt验证登录信息的客户端use_jwt_auth应为1
        :param adm:
        :return:
    '''

    use_jwt_auth = str_to_num(request.argget.all('use_jwt_auth', 0))
    if use_jwt_auth:

        # 使用jwt验证的客户端登出
        jwt_auth = JwtAuth()
        s,r = jwt_auth.clean_login()
        if s:
            data = {"msg": "Successfully logged out", "msg_type": "s", "code": 201,
                    "to_url": SITE_CONFIG["login_manager"]["LOGIN_OUT_TO"]}
        else:
            data = {"msg": r, "msg_type": "s", "code": 400}
    else:
        logout_user()

        data = {"msg":"Successfully logged out", "msg_type":"s", "code":201,
                "to_url":SITE_CONFIG["login_manager"]["LOGIN_OUT_TO"]}
    return response_format(data)


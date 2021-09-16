# -*-coding:utf-8-*-
from apps.configs.site_config import SITE_CONFIG
from apps.utils.format.obj_format import json_to_pyseq, str_to_num
from apps.views.user.process.sign_in import p_sign_in
from apps.views.user.process.sign_up import p_sign_up
from flask import request

def sign_up():

    if not SITE_CONFIG["login_manager"]["OPEN_REGISTER"]:
        data = {"msg":'Sorry, temporarily unregistered function',
                "code":401}
    else:
        email = request.argget.all('email','').strip()
        phone = request.argget.all('phone','').strip()
        username = request.argget.all('username','').strip()
        password = request.argget.all('password','').strip()
        password2 = request.argget.all('password2','').strip()
        code = request.argget.all('code','').strip()

        data = p_sign_up(email=email,
                         phone=phone,
                         username=username,
                         password=password,
                         password2=password2,
                         code=code)
    return data

def sign_in():

    username = request.argget.all('username','').strip()
    password = request.argget.all('password','').strip()
    code = request.argget.all('code','').strip()
    code_url_obj = json_to_pyseq(request.argget.all('code_url_obj',{}))
    remember_me = request.argget.all('remember_me', 0)
    use_jwt_auth = str_to_num(request.argget.all('use_jwt_auth', 0))
    try:
        remember_me = int(remember_me)
    except BaseException:
        data = {
            "msg": "remember_me requires an integer",
            "code": 400}
        return data

    data = p_sign_in(
        username=username,
        password=password,
        code_url_obj=code_url_obj,
        code=code,
        remember_me=remember_me,
        use_jwt_auth=use_jwt_auth)

    return data
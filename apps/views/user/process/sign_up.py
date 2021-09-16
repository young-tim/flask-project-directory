# -*-coding:utf-8-*-
from flask import request
from flask_login import current_user
from apps.app import db

from apps.configs.site_config import SITE_CONFIG
from apps.views.user.process.get_or_update_user import get_user, insert_user
from apps.utils.send_msg.send_email import send_email
from apps.utils.send_msg.send_sms import send_sms
from apps.utils.validation.str_format import email_format_ver, password_format_ver, short_str_verifi, mobile_phone_format_ver
from apps.models.user import UserModel, UserRoleModel
from apps.utils.verify.msg_verify_code import verify_code


def p_sign_up(username, password, password2, code, phone=None, email=None):
    """
    普通用户注册函数
    :param username:
    :param password:
    :param password2:
    :param code:
    :param phone:
    :param email:
    :return:
    """
    data = {}
    if current_user.is_authenticated:
        data['msg'] = "已登录"
        data["msg_type"] = "s"
        data["code"] = 201
        data['to_url'] = request.argget.all('next') or SITE_CONFIG["login_manager"]["LOGIN_IN_TO"]
        return data

    # 用户名格式验证
    s1, r1 = short_str_verifi(username, project="username")
    # 密码格式验证
    s2, r2 = password_format_ver(password)
    name_user = get_user(username=username)
    if not s1:
        data = {'msg':r1, 'msg_type':"e", "code":422}
    elif name_user:
        # 是否存在用户名
        data = {'msg': "用户名已存在", 'msg_type': "w", "code": 403}
    elif not s2:
        data = {'msg': r2, 'msg_type': "e", "code": 400}
        return data
    elif password2 != password:
        # 检验两次密码
        data = {'msg': "两个密码不一致", 'msg_type': "e", "code": 400}
    if data:
        return data

    if email:
        # 邮件注册
        # 邮箱格式验证
        s, r = email_format_ver(email)
        if not s:
            data = {'msg':r, 'msg_type':"e", "code":422}
        else:
            # 查询邮箱是否已存在
            email_user = get_user(email=email)
            if email_user:
                # 邮箱是否注册过
                data = {'msg': "该邮箱已注册，请更换邮箱或直接登录",
                        'msg_type': "w", "code": 403}
        if data:
            return data

        # 检验验证码
        r = verify_code(code=code, email=email)
        if not r:
            data = {'msg': "验证码错误", 'msg_type': "e", "code": 401}
            return data

    elif phone:
        # 手机注册
        # 手机号格式验证
        s, r = mobile_phone_format_ver(phone)
        if not s:
            data = {'msg': r, 'msg_type': "e", "code": 422}
        else:
            # 查询手机号是否已存在
            phone_user = get_user(telephone=phone)
            if phone_user:
                # 手机是否注册过
                data = {'msg': "该手机号已注册，请更换手机号或直接登录",
                        'msg_type': "w", "code": 403}
        if data:
            return data

        # # 检验验证码
        r = verify_code(code=code, phone=phone)
        if not r:
            data = {'msg': "验证码错误", 'msg_type': "e", "code": 401}
            return data

    if not data:
        # 用户基本信息
        user = UserModel(username=username,
                        email=email,
                        telephone = phone,
                        password=password
                        )
        # 插入默认角色
        role = UserRoleModel.query.filter_by(is_default=1).first()
        if role:
            role.users.append(user)

        res = insert_user(data=user)
        if res.id:
            if email:
                # 发送邮件
                subject = "注册成功通知"
                body = "欢迎注册 <b>{}</b>.<br><a>{}</a> 注册账号成功".format(
                    SITE_CONFIG["site_info"]["APP_NAME"],
                    email
                )
                data = {"title": subject,
                        "body": body,
                        "other_info": "End",
                        }
                # html = get_email_html(data)
                # send_email(subject=subject,
                #            recipients=[email],
                #            html_msg=html)
                send_email(subject=subject,
                           recipients=[email],
                           text_msg=body)
            elif phone:
                # 发送短信
                content = "[{}] Successful registration account.".format(
                    SITE_CONFIG["site_info"]["APP_NAME"])
                # TODO: 发送短信验证码未完成
                # send_sms(phone, content)

            data = {'msg':'注册成功',
                     'to_url':'/sign-in',
                    'msg_type':'s',"code":201}
        else:
            data = {'msg': 'Data saved incorrectly, please try again',
                    'msg_type': 'e', "code": 201}
        return data

    return data
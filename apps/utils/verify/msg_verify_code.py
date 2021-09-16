# -*-coding:utf-8-*-
import random
from flask import render_template, url_for
import time
from apps.core.template.get_template import get_email_html
from apps.utils.send_msg.send_email import send_email
from apps.configs.site_config import SITE_CONFIG
from apps.utils.send_msg.send_sms import send_sms
from apps.app import cache

"""
验证码生成及发送
"""

def _rndChar(i=2):
    """
    随机数字和字母
    :return:
    """
    if i == 1:
        # 字母
        an = random.randint(97, 122)
    else:
        # 数字
        an = random.randint(48, 57)
    return chr(an)


def create_code_send(account, account_type):
    """
    创建email和message验证码
    :param account:
    :param account_type:
    :return:
    """

    _str = ""
    type = SITE_CONFIG["verify_code"]["SEND_CODE_TYPE"]
    if type:
        temp_str_list = []
        # 如果存在设置
        if "string" in type and type["string"]:
            for t in range(int(type["string"])):
                c = _rndChar(i=1)
                temp_str_list.append(c)

        if "int" in type and type["int"]:
            for t in range(int(type["int"])):
                c = _rndChar(i=2)
                temp_str_list.append(c)
        # 打乱
        random.shuffle(temp_str_list)
        for c in temp_str_list:
            _str = "{}{}".format(_str, c)

    else:
        for t in range(6):
            i = random.randint(1, 2)
            c = _rndChar(i=i)
            _str = "{}{}".format(_str, c)

    if account_type == "email":
        _key = "verify_code_{}".format(account)
        _code = {
            'str': _str,
            'time': time.time(),
            'to_email': account,
            "type": "msg"}
        cache.set(_key, _code, SITE_CONFIG['verify_code']['EXPIRATION'])

        subject = "验证码 - {}".format(SITE_CONFIG['site_info']['APP_NAME'])
        data = {"title": subject,
                "body": email_code_html_body(_str),
                "other_info": "",
                }
        html = get_email_html(data)
        send_email(subject=subject,
                   recipients=[account],
                   html_msg=html
                   )
        return {"msg": "Has been sent. If not, please check spam",
                "msg_type": "s", "code": 201}

    elif account_type == "phone":
        _key = "verify_code_{}".format(account)
        _code = {
            'str': _str,
            'time': time.time(),
            'to_tel_number': account,
            "type": "msg"}
        cache.set(_key, _code, SITE_CONFIG['verify_code']['EXPIRATION'])

        content = """[{}] 您的验证码是： {} 。若非本人操作，请勿泄露""".format(SITE_CONFIG["site_info"]["APP_NAME"], _str)

        # TODO: 短信验证码未发送
        # s, r = send_sms([account])
        s,r = True, "短信验证码未发送，为了调试，当做 成功发放。"
        if not s:
            return {"msg": r, "msg_type": "w", "code": 400}

        return {"msg": r, "msg_type": "w", "code": 201}


def email_code_html_body(code):
    """
    邮箱验证码正文的html拼接
    :param: 验证码
    :return:
    """

    body = """
        <span>{}:</span><br>
        <span style="color: #69B922; font-size: 20px;text-align: center;">
                {}
        </span><br>
        <span>{}</span><br>
        """.format('您的验证码是', code,
        '切勿将验证码告诉其他人。',
        '如果不是您发送的，请忽略它。')
    return body


def verify_code(code, email="", phone=""):
    """
    验证email或message验证码
    :param code: 验证码
    :param email: 邮箱
    :param phone: 手机号
    :return:
    """
    r = False
    if not code:
        return r
    _key = ""
    _code = None
    if email:
        _key = "verify_code_{}".format(email)
        _code = cache.get(_key)

    elif phone:
        _key = "verify_code_{}".format(phone)
        _code = cache.get(_key)

    if _code:
        if _code['str'].lower() == code.lower() and \
                                time.time() - _code['time'] < SITE_CONFIG["verify_code"]["EXPIRATION"]:
            cache.delete(_key)
            r = True

    return r

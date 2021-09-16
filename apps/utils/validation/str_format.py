# -*-coding:utf-8-*-
from flask_login import current_user
import regex as re
from apps.core.flask.reqparse import arg_verify


def short_str_verifi(short_str, project=None, allow_special_chart=False):
    """
    各种名字短字符串验证
    Character name to verify
    :param s:
    allow_special_chart: 是否允许特殊字符
    :return:
    """

    s, r = arg_verify(reqargs=[("name", short_str)], required=True)
    if not s:
        return False, r["msg"]

    if not allow_special_chart:
        if re.search(r"[\.\*#\?]+", short_str):
            return False, "The name format is not correct,You can't use '.','*','#','?'"

    return True, ""


def email_format_ver(email):
    """
    邮箱字符验证
    Character email to verify
    :param email:
    :return:
    """

    if re.search(
        r"^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$",
            email):
        return True, ""
    else:
        return False, "The email format is not correct"


def mobile_phone_format_ver(number):
    """
    手机号字符验证
    Character mobile phone to verify
    :param number:
    :return:
    """

    if re.search(r"^[0-9]{11}$", number):
        return True, ""
    else:
        return False, "The phone format is not correct"


def url_format_ver(url):

    if re.search(
        r"(http|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?",
            url):
        return True, ""
    else:
        return False, "The url format is not correct"


def password_format_ver(password):
    """
    密码格式检验
    :param password:
    :return:
    """

    if len(password) < 6:
        return False, 'Password at least 6 characters! And at least contain Numbers, letters, special characters of two kinds'
    else:
        too_simple = True
        last_ac = False
        for p in password:
            _ac = ord(p)
            if last_ac:
                if _ac != last_ac + 1:
                    too_simple = False
                    break
            last_ac = _ac
        if too_simple:
            return False, 'The password is too simple, can not use continuous characters!'
    return True, ""

def ip_format_ver(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True, ""
    else:
        return False, "IP格式不正确"

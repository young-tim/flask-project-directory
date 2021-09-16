# -*-coding:utf-8-*-
import datetime
from flask import request
from flask_login import current_user
from apps.models.sys import SysCallRecordModel
from apps.app import db
from apps.core.flask.reqparse import arg_verify
from apps.configs.site_config import SITE_CONFIG
from apps.views.user.process.get_or_update_user import get_user
from apps.utils.format.obj_format import json_to_pyseq, str_to_num
from apps.utils.validation.str_format import email_format_ver, mobile_phone_format_ver
from apps.utils.verify.img_verify_code import create_img_code, verify_image_code
from apps.utils.verify.msg_verify_code import create_code_send


def send_code():
    """
    发送验证码
    :return:
    """
    data = {}
    account_type = request.argget.all('account_type', "email").strip()
    account = request.argget.all('account')
    exist_account = str_to_num(request.argget.all('exist_account', 0))
    code = request.argget.all('code', '').strip()
    code_url_obj = json_to_pyseq(request.argget.all('code_url_obj', {}))

    s, r = arg_verify(reqargs=[("account_type", account_type)],
                      only=["email", "phone"])
    if not s:
        return r

    if account_type == "email":
        s, r = arg_verify(reqargs=[("Email", account)], required=True)
        if not s:
            return r
        # 邮箱格式验证
        r, s = email_format_ver(account)
        if not r:
            data = {'msg': s, 'msg_type': "e", "code": 422}
            return data

        if exist_account:
            if not get_user(email=account):
                data = {
                    'msg': "This account is not registered on this platform",
                    'msg_type': "w",
                    "code": 400}
                return data

        r, s = call_verification(code_url_obj, code)
        if not r:
            return s
        data = create_code_send(account=account, account_type=account_type)

    elif account_type == "phone":
        s, r = arg_verify(
            reqargs=[
                ("Telephone number", account)], required=True)
        if not s:
            return r

        # 移动号码格式格式验证
        r, s = mobile_phone_format_ver(account)
        if not r:
            data = {'msg': s, 'msg_type': "e", "code": 422}
            return data

        if exist_account:
            user_query = {"telephone": account}
            if not get_user(telephone=account):
                data = {
                    'msg': "This account is not registered on this platform",
                    'msg_type': "w",
                    "code": 400}
                return data

        r, s = call_verification(code_url_obj, code)
        if not r:
            return s
        data = create_code_send(account=account, account_type=account_type)

    return data


def call_verification(code_url_obj, code):
    """
    记录调用次数,并查看是否有调用权限
    :return:
    """

    # 记录调用
    if current_user.is_authenticated:
        user_id = current_user.str_id
    else:
        user_id = ''
    record = SysCallRecordModel(type='api',
                                req_path=request.path,
                                ip=request.remote_addr,
                                user_id=user_id)
    db.session.add(record)
    db.session.commit()

    # 计算当前时间的前一分钟
    tc = datetime.datetime.now() - datetime.timedelta(minutes=1)
    # 查找1分钟内本IP的调用次数
    freq = SysCallRecordModel.query.filter_by(type='api',
                                              req_path=request.path,
                                              ip=request.remote_addr,
                                              user_id=user_id) \
                                    .filter(tc < SysCallRecordModel.create_time)\
                                    .count()
    if freq:
        if freq > SITE_CONFIG["verify_code"]["MAX_NUM_SEND_SAMEIP_PERMIN"]:
            # 大于单位时间最大调用次数访问验证
            data = {
                'msg': "The system detects that your network is sending verification codes frequently. Please try again later!",
                'msg_type': "w",
                "code": 401}
            return False, data

        elif freq > SITE_CONFIG["verify_code"]["MAX_NUM_SEND_SAMEIP_PERMIN_NO_IMGCODE"] + 1:
            # 已超过单位时间无图片验证码情况下的最大调用次数, 验证图片验证码
            # 检验图片验证码
            r = verify_image_code(code_url_obj, code)
            if not r:
                data = {
                    'msg': "Image verification code error, email not sent",
                    'msg_type': "e",
                    "code": 401}
                # 验证错误,开启验证码验证
                data["open_img_verif_code"] = True
                data["code"] = create_img_code()
                del data["code"]["str"]
                return False, data

        elif freq > SITE_CONFIG["verify_code"]["MAX_NUM_SEND_SAMEIP_PERMIN_NO_IMGCODE"]:
            # 如果刚大于单位时间内，无图片验证码情况下的最大调用次数, 返回图片验证码验证码
            data = {
                'msg': "系统检测到您的操作过于频繁，请输入图形验证码。",
                'msg_type': "w",
                "code": 401}

            data["open_img_verif_code"] = True
            data["code"] = create_img_code()
            del data["code"]["str"]
            return False, data

    return True, ""

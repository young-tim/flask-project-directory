# -*-coding:utf-8-*-
from flask import request, session
from flask_login import current_user, login_user
import datetime
from apps.core.auth.jwt_auth import JwtAuth
from apps.utils.validation.str_format import email_format_ver, mobile_phone_format_ver
from apps.utils.verify.img_verify_code import verify_image_code
from apps.app import db
from apps.models.user import UserModel, UserLoginLogModel
from apps.configs.site_config import SITE_CONFIG


def p_sign_in(username, password, code_url_obj, code, remember_me, use_jwt_auth=0):

    '''
    用户登录函数
    :param :
    :return:
    '''
    data = {}
    if current_user.is_authenticated and username in [current_user.username,
                                                      current_user.email,
                                                      current_user.telephone]:
        data['msg'] = "用户已登录"
        data["msg_type"] = "s"
        data["code"] = 201
        data['to_url'] = request.argget.all('next') or SITE_CONFIG["login_manager"]["LOGIN_IN_TO"]
        data["data"] = current_user.user_info

        # 记录登录日志
        add_login_log(current_user, client=None, login_account=username, login_msg=data['msg'])

        return data

    # name & pass
    s, r = email_format_ver(username)
    s2, r2 = mobile_phone_format_ver(username)
    uq = [UserModel.is_delete == 0]
    if s:
        uq.append(UserModel.email == username)
    elif s2:
        uq.append(UserModel.telephone == username)
    else:
        uq.append(UserModel.username == username)

    user = UserModel.query.filter(*uq).order_by(UserModel.create_time.desc()).first()
    if not user:
        # TODO: 需要注意，当有人不断用账号轮询爆破登录时，不会受到同一用户多次密码错误限制的约束。需要处理该种情况
        # 用户不存在
        data = {"msg":"账号或密码错误", "code":401}
        # 记录登录日志
        add_login_log(user, login_account=username, login_msg="账号不存在")
        return data

    # 判断是否多次密码错误,是就要验证图片验证码
    PW_WRONG_NUM_IMG_CODE = SITE_CONFIG["login_manager"]["PW_WRONG_NUM_IMG_CODE"]

    if user.last_login_time is not None and user.login_error_num >= PW_WRONG_NUM_IMG_CODE:
        if not code:
            data['msg'] = "请输入图片验证码"
            data['open_img_verif_code'] = True
            data['code'] = 401
            return data

        # 图片验证码验证
        r = verify_image_code(code_url_obj, code)
        if not r:
            data["open_img_verif_code"] = True
            data['msg'] = "图片验证码错误"
            data["code"] = 401
            return data

    # 密码验证
    if user and user.check_password(password) and not user.is_delete:
        if user.is_active:
            if use_jwt_auth:
                # 使用的是jwt验证
                # 获取token
                jwt_auth = JwtAuth()
                data["auth_token"] = jwt_auth.get_login_token(user)
                client = "app"
            else:
                session[SITE_CONFIG['system']['USER_ID']] = user.id
                if remember_me:
                    # 如果记住我，session过期时间默认为31天
                    session.permanent = True
                login_user(user, remember_me)
                client = "browser"

            data['msg'] = "登录成功"
            data["code"] = 201
            data["to_url"] = request.argget.all('next') or SITE_CONFIG["login_manager"]["LOGIN_IN_TO"]
            data["data"] = current_user.user_info

            # 记录登录日志
            add_login_log(user, client, login_account=username, login_msg=data['msg'])

            return data

        # 未激活
        data['msg'] = "帐户已停用或冻结"
        data["msg_type"] = "w"
        data["code"] = 401

        # 记录登录日志
        add_login_log(user, pass_error=1, login_account=username, login_msg=data['msg'])

    else:
        #　密码错误

        if use_jwt_auth:
            # 使用的是jwt验证
            client = "app"
        else:
            client = "browser"

        # 判断是否多次密码错误
        if user.last_login_time is not None and user.login_error_num >= PW_WRONG_NUM_IMG_CODE:
            # 图片验证码验证码
            data["open_img_verif_code"] = True
        data['msg'] = "账号或密码错误"
        data["msg_type"] = "e"
        data["code"] = 401

        # 记录登录日志
        add_login_log(user, client, pass_error=1, login_account=username, login_msg=data['msg'])

    return data


def add_login_log(user, client=None, pass_error=0, login_account=None, login_msg=None):
    '''
    添加登录日志
    :param user: 用户对象实例
    :param pass_error: 登录结果：0 成功，1 失败
    :param client: 登录客户端
    :param login_account: 登录账号
    :param login_msg: 登录信息
    :return:
    '''
    user_login_log = UserLoginLogModel(pass_error=pass_error,
                                       ip=request.remote_addr,
                                       client=client,
                                       login_account=login_account,
                                       login_msg=login_msg)

    if user:
        if pass_error:
            user.login_error_num += 1
        else:
            user.login_error_num = 0
        user.last_login_time = datetime.datetime.now()

    user_login_log.user = user

    db.session.add(user_login_log)
    db.session.commit()

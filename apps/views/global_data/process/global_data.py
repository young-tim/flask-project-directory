# -*-coding:utf-8-*-
# from bson import ObjectId
from flask_login import current_user
from apps.configs.config import VERSION
from apps.configs.site_config import SITE_CONFIG
from apps.core.flask.restful import succcess


def get_global_site_data(req_type="api"):

    '''
    获取全局的站点信息
    req_type:如果为"view"则不需要返回用户基本信息
    :return:
    '''
    data = {}

    # 全局数据
    data["site_info"] = SITE_CONFIG["site_info"]
    data["site_info"] = dict(data["site_info"], **SITE_CONFIG["seo"])
    data["site_info"]["SYS_VERSION"] = VERSION

    if req_type != "view":
        # 假如用户已登录且身份验证成功
        if current_user.is_authenticated:
            user_info = current_user.user_info

            data["is_authenticated"] = True
            data["user_info"] = user_info
        else:
            data["is_authenticated"] = False
            data["user_info"] = {}

    return succcess(data)


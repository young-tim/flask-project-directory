# encoding:utf-8
# -*-coding:utf-8-*-
from importlib import import_module
from flask import Blueprint
from apps.configs.config import API_URL_PREFIX, STATIC_PATH, STATIC_URL_PREFIX

'''
蓝本:配置路由,url
'''
main = Blueprint('main', __name__)
api = Blueprint('api', __name__, url_prefix=API_URL_PREFIX)
static = Blueprint('static', __name__, url_prefix=STATIC_URL_PREFIX,
                   template_folder=STATIC_PATH,
                   static_folder=STATIC_PATH)

# 引入路由
routing_moudel = [
    {"from": "apps.views.index", "import": ["index"]},
    # {"from": "apps.views.global_data", "import": ["global_data"]},
    # {"from": "apps.views.token", "import": ["rest_token"]},
    # {"from": "apps.views.user", "import": ["sign", 'userInfo']},
    # {"from": "apps.views.verification_code", "import": ["code"]},
]

for rout_m in routing_moudel:
    for im in rout_m["import"]:
        moudel = "{}.{}".format(rout_m["from"], im)
        import_module(moudel)

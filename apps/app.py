#encoding:utf-8
from apps.core.flask.flask_app import App
from apps.core.flask.cache import Cache
from apps.core.flask.rest_session import RestSession
from apps.core.logger.web_logging import WebLogger
from flask_mail import Mail
from flask_oauthlib.client import OAuth
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from redis import StrictRedis
from apps.configs.db_config import DB_CONFIG
from flask_sqlalchemy import SQLAlchemy
from apps.utils.sms_platform.alidayu import AlidayuAPI
from flask_docs import ApiDoc
from flask_cors import CORS


'''
 Flask app 与其他核心模块实例化，避免循环引用。
 注意: 不要将模块初始化设置放在本文件
'''
# 主程序
app = App(__name__)
cache = Cache()
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
session = Session()
rest_session = RestSession()
mail = Mail()
alidayu = AlidayuAPI()  # 短信(阿里大鱼)操作对象
weblog = WebLogger()
oauth = OAuth()
redis = StrictRedis(host=DB_CONFIG["redis"]["host"][0],
                    port=DB_CONFIG["redis"]["port"][0],
                    password=DB_CONFIG["redis"]["password"])
api_doc = ApiDoc()
cors = CORS()

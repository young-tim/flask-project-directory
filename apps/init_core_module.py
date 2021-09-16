#encoding:utf-8
import apps.configs.config as config
from apps.configs.db_config import DB_CONFIG
from apps.utils.format.obj_format import ConfDictToClass
from apps.configs.site_config import SITE_CONFIG
from apps.core.db.database_config import MysqlConfig
from apps.app import cache, db, mail, redis, weblog, session, rest_session, login_manager, csrf, oauth, alidayu, api_doc, cors
from apps.core.blueprint import main, static, api
from apps.core.flask.request import RequestProcess
from apps.core.flask.routing import RegexConverter
from apps.core.flask.errorhandler import ErrorHandler


'''
初始化一些核心模块
'''

def init_core_module(app):

    '''
    初始化核心模块
    :param app:
    :return:
    '''

    # 初始化配置文件
    app.config.from_object(config)

    # 数据库
    app.config.from_object(MysqlConfig())
    db.init_app(app)

    # 缓存
    app.config.from_object(ConfDictToClass(SITE_CONFIG["cache"]))
    app.config["CACHE_REDIS"] = redis
    # cache.init_app(app)

    # 最大请求大小
    app.config["MAX_CONTENT_LENGTH"] = SITE_CONFIG["system"]["MAX_CONTENT_LENGTH"] * 1024 * 1024
    # Session会话配置
    app.config.from_object(ConfDictToClass(SITE_CONFIG["session"]))
    app.config["SESSION_REDIS"] = redis
    # session.init_app(app)
    # rest_session.init_app(app)

    # Csrf token
    csrf.init_app(app)

    # 允许前端跨域
    # r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
    cors.init_app(app, supports_credentials=True, resources=r'/*')

    # 登录管理
    login_manager.init_app(app)
    # login_manager.anonymous_user = AnonymousUser()
    login_manager.session_protection = app.config['SESSION_PROTECTION']
    # 日志
    weblog.init_app(app)
    # Oauth
    oauth.init_app(app)

    # 让路由支持正则
    app.url_map.converters['regex'] = RegexConverter

    # 邮件
    app.config.from_object(ConfDictToClass(SITE_CONFIG['EMAIL']))
    mail.init_app(app)

    # 短信(阿里大鱼)初始化
    alidayu.init_app(app)

    # 注册蓝图 blueprint
    app.register_blueprint(static)
    app.register_blueprint(main)
    app.register_blueprint(api)

    # 请求处理
    request_process = RequestProcess()
    request_process.init_request_process(app=app)

    # 错误处理
    ErrorHandler(app)

    # flask-docs注册：自动生成api文档
    api_doc.init_app(app)

#-*-coding:utf-8-*-
import logging
import os

curren_path = os.path.abspath(os.path.dirname(__file__))


"""
#################################################
系统配置文件，一般无需改动。
#################################################
"""

'''
系统版本
'''
VERSION = "0.1 Beta"

'''
  需要导入的模块
'''
MODULES = ["apps.views.user.process.load_user_request"]
# MODULES = []

'''
 项目各路径配置PATH
'''
PROJECT_PATH = os.path.abspath("{}/../..".format(curren_path))
APPS_PATH = os.path.abspath("{}/apps".format(PROJECT_PATH))
STATIC_PATH = os.path.abspath("{}/static".format(APPS_PATH))
CONFIG_PATH = os.path.abspath("{}/configs".format(APPS_PATH))

'''
路由,不要以"/"结尾
'''
API_URL_PREFIX = "/api"
STATIC_URL_PREFIX = "/static"

'''
 权限permission
'''

'''
 固定KEY的缓存配置
'''
# SecretToken缓存key与超时
REST_SECRET_TOKEN_CACHE_KEY = "web_secret_token"
REST_SECRET_TOKEN_CACHE_TIMEOUT = 3600*24

# config.py中的CONFIG缓存配置
CONFIG_CACHE_KEY = "web_get_config"
# 配置的缓存时间,主要是为了当你修改了CONFIG_CACHE_KEY后,老的配置缓存未清理，过期自动清理
CONFIG_CACHE_TIMEOUT = 3600*24 # 单位s


'''
 日志 log
'''
LOG_PATH = "{}/logs".format(PROJECT_PATH)
# 日志文件名，请勿加文件后缀
WEBLOG_NORMAL_FILENAME = "web_log"
WEBLOG_EXCEP_FILENAME = "error"
# 日志文件后缀名，日志会在文件名和后缀之间加入日期
LOG_FILENAME_SUFFIX = "log"
LOG_FORMATTER = "[%(asctime)s] [%(levelname)s] %(message)s"
# 日志正常级别，生产环境建议换成 INFO
WEBLOG_NORMAL_LEVEL = logging.DEBUG
# 日志异常级别，生产环境建议换成 ERROR
WEBLOG_EXCEP_LEVEL = logging.INFO
# 如果为True则错误日志中不写入"详细的错误", 只写入错误类型
PRESERVE_CONTEXT_ON_EXCEPTION = False

'''
 Request
'''
# 不存在的请求警告
METHOD_WARNING = "405, The method is not allowed for the requested URL"

'''
 针对浏览器访问的Session设置
'''
# 会话保护属性,strong或者basic
SESSION_PROTECTION = "strong"
SESSION_COOKIE_PATH = "/"
# 控制是否应该使用安全标志设置cookies
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
# 设置参数SESSION_USE_SIGNER为True时,请保证session初始化前app.config中有SECRET_KEY
SESSION_USE_SIGNER = True
SECRET_KEY = "hg@*(!Ig0920h07Hs341g"

'''
 Cache配置
'''
# cache 固定key
GET_DEFAULT_SYS_PER_CACHE_KEY = "sys_permissions_default"
GET_ALL_PERS_CACHE_KEY = "sys_permissions"

'''
 *安全
'''
# CSRF配置, 只对普通浏览器请求验证有效, 对使用RestToken验证的请求无效
WTF_CSRF_TIME_LIMIT = 3600*2
CSRF_ENABLED = False    # 这里关闭, 请通过API_TOKEN_ENABLED配置项开启（或在@app.before_request再选择性开启需要验证token的请求）
WTF_CSRF_CHECK_DEFAULT = False  # 这里关闭, 请通过API_TOKEN_ENABLED配置项开启（或在@app.before_request再选择性开启需要验证token的请求）
WTF_CSRF_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
FRONT_CSRF_ENABLED = True   # 是否自动给前端设置csrf token
API_TOKEN_ENABLED = False   # 是否开启接口的token验证

'''
阿里大于（云通信）配置参数
'''
ALIDAYU_APP_KEY = ''
ALIDAYU_APP_SECRET = ''
ALIDAYU_SIGN_NAME = ''
ALIDAYU_TEMPLATE_CODE = ''

'''
登录
'''
LOGIN_DISABLED = False
# 第三方登录插件支持："wechat", "qq", "sina_weibo", "alipay","github", "facebook", "twitter"……
LOGIN_PLATFORM = []

'''
flask-docs：自动生成api文档配置
文档查看地址：localhost/docs/api
'''
# 本地加载
# API_DOC_CDN = False
# 禁用文档页面: True 启用，False 禁用
API_DOC_ENABLE = True
# 需要显示文档的 Api
API_DOC_MEMBER = ['api', 'open_api']
# 需要排除的 RESTful Api 文档
RESTFUL_API_DOC_EXCLUDE = []

'''
其他
'''
# 默认字体路径, 用于生成验证码的
FONT_PATH = "{}/font/".format(STATIC_PATH)
FONT_TYPES = ["Arial.ttf", "angelina.ttf", "LHANDW.TTF", "verdana.ttf"]
VIOLATION_IMG_PATH = "{}/sys_imgs/violation.png".format(STATIC_PATH)
# 最高权限位，如权限位不够，可扩充。但需要注意数据库字段长度限制及以前开发者的权限位也需更新
SUPER_PER = 0b1111111111111111111111111111111
# 必须保留权限
PRESERVE_PERS = ["GENERAL_USER","ROOT", "ADMIN", "STAFF"]

# flask-pagination（分页）配置参数
PER_PAGE = 10 #每页数据条数

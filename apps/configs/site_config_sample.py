#encoding:utf-8
"""
################################################################################
站点配置文件，一般业务上的全局变量放在此，可根据业务内容进行调整。
###############################################################################
"""

SITE_CONFIG = {
    # 站点基础设置: APP(Web)全局数据设置
    # 此模块所有的KEY值, 都可以直接请求全局Api(/api/global)获取.也可以直接在主题中使用Jinjia2模板引擎获取(g.site_global.site_info.XXXX)
    "site_info": {
        "STATIC_FILE_VERSION": 20180404041316,  # 静态文件版本(当修改了CSS,JS等静态文件的时候，修改此版本号)

        "APP_NAME": "",     # APP(站点)名称,将作为全局变量使用在平台上
        "SITE_NAME": "", # 站点名称
        "SITE_URL": "",  # Web站点URL(如果没有填写, 则使用默认的当前域名首页地址)
        "TITLE_PREFIX": "",     # APP(Web)Title前缀
        "TITLE_SUFFIX": "",     # APP(Web)Title后缀
        "TITLE_PREFIX_ADM": "",     # APP(Web)管理端Title前缀
        "TITLE_SUFFIX_ADM": "-管理端",    # APP(Web)管理端Title后缀

        # "PC_LOGO_DISPLAY": "logo",  # PC端用App name 还是Logo image 作为APP(Web)的Logo显示, 为空则显示Logo和App name。可填logo或name(需要主题支持)
        # "MB_LOGO_DISPLAY": "name",   # 移动端用App name 还是Logo image 作为APP(Web)的Logo显示, 为空则App name优先。可填logo或name(需要主题支持)
        # "LOGO_IMG_URL": "/static/sys_imgs/logo.png",    # APP(Web)Logo的URL
        # "LOGO_IMG_URL_SECONDAEY": "/static/sys_imgs/logo-2.png",  # APP(Web)Logo URL备用(需要主题支持)
        # "FAVICON": "/static/sys_imgs/logo.ico",  # APP(Web)favicon图标的URL

        # "HEAD_CODE": "",    # 用于放入html中 head标签内的js/css/html代码(如Google分析代码/百度统计代码)
        # "FOOTER_CODE": "",  # 用于放入html中 body标签 内的js/css/html代码(如Google分析代码/百度统计代码)

        # 友情链接:值(Value)格式为{'url':'友情链接', 'logo_url':'logo链接'}
        "FRIEND_LINK": {
                "Github": {
                    "url": "www.aliyun.com",
                    "level": 1,
                    "icon_url": "",
                    "aliases": "Github"
                },
                "阿里云": {
                    "url": "www.aliyun.com",
                    "level": 1,
                    "icon_url": "",
                    "aliases": "阿里云"
                },
                "七牛云": {
                    "url": "www.aliyun.com",
                    "level": 1,
                    "icon_url": "",
                    "aliases": "七牛云"
                },
                "码云": {
                    "url": "www.aliyun.com",
                    "level": 1,
                    "icon_url": "",
                    "aliases": "码云"
                }
        },
    },
    # 针对网页客户端的简单的SEO配置
    # 此模块所有的KEY值, 都可以直接请求全局Api(/api/global)获取.也可以直接在主题中使用Jinjia2模板引擎获取(g.site_global.site_config.XXXX)
    "seo": {
        "DEFAULT_KEYWORDS": "keywordk",    # 网站的页面默认关键词
        "DEFAULT_DESCRIPTION": "description",    # 网站的页面默认简单描述
    },
    # 验证码设置
    "verify_code": {
        "MAX_IMG_CODE_INTERFERENCE": 20,    # 图片验证码干扰程度的最大值
        "MIN_IMG_CODE_INTERFERENCE": 10,    # 图片验证码干扰程度的最小值,最小值小于10时无效
        "EXPIRATION": 600,  # 验证码过期时间(s)
        # 发送的验证码 字符类型：字符个数
        "SEND_CODE_TYPE": {
            "string": 0,
            "int": 6
        },
        # 同一IP地址,同一用户(未登录的同属同一匿名用户),允许每分钟在不验证[图片验证码]的时候,调用API发送验证码最大次数。
        # 超过次数后API会生成[图片验证码]并返回图片url对象(也可以自己调用获取图片验证码API获取)。
        # 如果你的客户端不支持显示图片验证码,请设置此配置为99999999。
        "MAX_NUM_SEND_SAMEIP_PERMIN_NO_IMGCODE": 1,
        "IMG_CODE_DIR": "upload/verify_code",    # 图片验证码保存目录，在static/upload <save_dir>目录下
        "MAX_NUM_SEND_SAMEIP_PERMIN": 5,   # 同一IP地址,同一用户(未登录的同属一匿名用户), 允许每分钟调用API发送验证码的最大次数
    },
    # 短信设置
    "sms": {
        # 短信模板
        "sms_templates": {
            # 短信验证码
            "verify_code": [
                {
                    "platform": "alidayu",  # 短信平台
                    "template_code": "",   # 短信模板编码
                    "sign_name": "",    # 短信签名
                    "content": "",  # 短信模板内容
                    # 短信模板参数
                    "param": [
                        "code"
                    ]
                }
            ],
            # 通知短信
            "notification": [],
            # 营销短信
            "marketing": []
        }
    },
    # 邮箱信息
    "EMAIL": {
        "MAIL_USERNAME": "xxx@xxx.com",    # 邮箱用户名
        "MAIL_DEFAULT_SENDER": ("name", "xxx@xxx.com"), # 邮箱名称、邮箱地址
        "MAIL_PASSWORD": "xxxx",    # 邮箱密码
        "MAIL_SERVER": "smtp.qq.com",   # 邮箱服务器
        "MAIL_PORT": "587",     # 邮箱服务器端口
        "MAIL_USE_TLS": True  # True or False   是否适用TLS
    },
    # 登录信息
    "login_manager": {
        "LOGIN_VIEW": "/sign-in",   # 需要登录的页面,未登录时,api会响应401,并带上需要跳转到路由to_url
        "LOGIN_IN_TO": "/",     # 登录成功后,api会响应数据会带上需要跳转到路由to_url
        "LOGIN_OUT_TO": "/",    # 退出登录后,api会响应数据会带上需要跳转到路由to_url
        "OPEN_REGISTER": True,   # 开放注册
        "PW_WRONG_NUM_IMG_CODE": 6 # 同一用户登录密码错误几次后，响应图形验证码, 并且需要验证
    },
    # 操作日志设置
    "weblogger": {
        "SING_IN_LOG_KEEP_NUM": 30,     # 登录日志保留个数
        "USER_OP_LOG_KEEP_NUM": 30,     # 用户操作日志保留个数
    },
    # auth\token 参数设置
    "rest_auth_token": {
        "MAX_SAME_TIME_LOGIN": 3,   # 最多能同时登录几个使用JWT验证的客户端,超过此数目则会把旧的登录注销
        "LOGIN_LIFETIME": 2592000,  # jwt 登录BearerToken有效期(s)，默认2592000秒=30天
        "REST_ACCESS_TOKEN_LIFETIME": 172800,   # 给客户端发补的访问Token AccessToken的有效期
    },
    # 缓存设置
    "cache": {
        "USE_CACHE": True,  # 是否使用缓存功能,建议开启
        "CACHE_TYPE": "redis",   # 缓存使用的类型,可选择redis,mongodb
        "CACHE_DEFAULT_TIMEOUT": 600,   # (s秒)默认缓存时间,当单个缓存没有设定缓存时间时会使用该时间
        "CACHE_KEY_PREFIX": "sys_cache_",     # 所有键(key)之前添加的前缀,这使得它可以为不同的应用程序使用相同的memcached(内存)服务器
        "CACHE_MONGODB_COLLECT": "sys_cache_"  # 保存cache的collection,当CACHE_TYPE为mongodb时有效
    },
    # Session参数设置
    "session": {
        "SESSION_TYPE": "redis",  # 保存Session会话的类型,可选mongodb, redis
        "SESSION_PERMANENT": True,  # 是否使用永久会话
        "PERMANENT_SESSION_LIFETIME": 2592000,  # 永久会话的有效期
        "SESSION_KEY_PREFIX": "sys_session_",   # 添加一个前缀,之前所有的会话密钥。这使得它可以为不同的应用程序使用相同的后端存储服务器
        "SESSION_MONGODB_COLLECT": "sys_session_",  # Mongodb保存session的collection,当SESSION_TYPE为mongodb时有效
    },
    # 文件上传配置
    "upload": {
        # 上传:允许上传的文件后缀(全部小写),每个用英文的','隔开
        "UP_ALLOWED_EXTENSIONS": [
                "xls",
                "xlxs",
                "doc",
                "docx",
                "ppt",
                "pptx",
                "txt",
                "pdf",
                "png",
                "jpg",
                "jpeg",
                "gif",
                "ico",
                "mp4",
                "rmvb",
                "avi",
                "mkv",
                "mov",
                "mp3",
                "wav",
                "wma",
                "ogg",
                "zip",
                "gzip",
                "tar"
            ],
        "SAVE_DIR": "upload",    # 上传:保存目录，如果存在'/'则会自动切分创建子目录
    },
    # 其他web系统参数设置
    "system": {
        "KEY_HIDING": True,     # 开启后,管理端通过/api/admin/xxx获取到的数据中，密钥类型的值，则会以随机字符代替。 如某个插件配置中有密码, 不想让它暴露在浏览器, 则可开启.
        "TEMPLATES_AUTO_RELOAD": True,  # 是否自动加载页面(html)模板.开启后,每次html页面修改都无需重启Web
        "MAX_CONTENT_LENGTH": 50.0,     # 拒绝内容长度大于此值的请求进入，并返回一个 413 状态码(单位:Mb)
        "USER_ID": "79mpHSZIuqbGrFWh",  # 用于记录用户登录状态的session key
    }
}

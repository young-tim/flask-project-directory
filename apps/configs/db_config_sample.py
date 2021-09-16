#encoding:utf-8

"""
#################################################
数据库配置文件，一般无需改动。
#################################################
"""

DB_CONFIG = {
    "mysql": {
        "host": "127.0.0.1",
        "port": "3306",
        "username": "<username>",
        "password": "<password>",
        "database": "<database>",
        "charset": "utf8mb4",
        "prefix": ""    # 数据表前缀
    },
    "redis": {
        "host": [
            "127.0.0.1"
        ],
        "port": [
            "6379"
        ],
        "password": ""
    }
}

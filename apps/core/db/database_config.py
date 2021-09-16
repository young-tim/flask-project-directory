#encoding:utf-8
from apps.configs.db_config import DB_CONFIG

class MysqlConfig():
    DB_HOST = DB_CONFIG['mysql']['host']
    DB_PORT = DB_CONFIG['mysql']['port']
    DB_USERNAME = DB_CONFIG['mysql']['username']
    DB_PASSWORD = DB_CONFIG['mysql']['password']
    DB_DATABASE = DB_CONFIG['mysql']['database']
    DB_CHARSET = DB_CONFIG['mysql']['charset']
    DB_URL = "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_DATABASE,DB_CHARSET)

    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
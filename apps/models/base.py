#encoding: utf-8
from apps.app import db
from apps.configs.db_config import DB_CONFIG
from datetime import datetime
import time
import copy
from sqlalchemy.ext.declarative import declared_attr
from apps.app import weblog


class BaseModel(db.Model):
    """
    设为db基类
    """
    # Flask-SQLAlchemy创建table时,如何声明基类（这个类不会创建表,可以被继承）
    # 方法就是把__abstract__这个属性设置为True,这个类为基类，不会被创建为表！
    __abstract__ = True

    # 添加配置设置编码
    # __table_args__ = {
    #     'mysql_charset': DB_CONFIG['mysql']['charset']
    # }

    @declared_attr
    def __tablename__(cls):
        # 将表类名自动小写，_分割，去掉末尾的"Model"字样
        if "_" in cls.__name__:
            name =cls.__name__
        else:
            name = ''.join([('_' + ch.lower()) if ch.isupper() else ch
                    for ch in cls.__name__]).strip('_')
            if name[-6:] == "_model":
                name = name[:-6]

        _table_prefix = DB_CONFIG['mysql']['prefix']
        return _table_prefix + name if _table_prefix else name

    # 每个表都自动带上创建时间、更新时间
    create_time = db.Column(db.Integer, default=time.time, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')


    def toDict(self):
        """
        返回dict结果
        用法：
            r = model.query.……
            > r.toDict()  # 输出dict结果数据
            > r.toDict().__str__()    # 输出字符串结果数据
        :return: c_dict
        """
        # 使用深拷贝，避免引用对象self.__dict__缺少"_sa_instance_state"属性
        c_dict = copy.deepcopy(self.__dict__)
        for (k, v) in c_dict.items():
            # 将datetime内容格式化为[Y-m-d H:M:S]
            if isinstance(v, datetime):
                c_dict[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        try:
            if "_sa_instance_state" in c_dict:
                del c_dict["_sa_instance_state"]
            # if "create_time" in c_dict:
                # del c_dict["create_time"]
            if "update_time" in c_dict:
                del c_dict["update_time"]
        except Exception as e:
            weblog.err(e)

        return c_dict
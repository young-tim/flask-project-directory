#encoding:utf-8
# 存放所有数据模型的枚举类数据
import enum
from apps.configs.config import SUPER_PER


class GenderEnumModel(enum.Enum):
    # 性别枚举
    UNKNOW = 0      # 未知
    MALE = 1        # 男性
    FEMALE = 2      # 女性
    SECRET = 3      # 秘密

class DomainEnumModel(enum.Enum):
    # 站点域（即支持使用的终端平台）枚举
    USER = 0      # 用户端，仅能用于用户端平台
    ADMIN = 1     # 管理端，可登陆管理平台

class UserPersmissionEnumModel(enum.Enum):
    # 一般仅在数据初始化时用到，其他正常使用过程中，请使用UserPermissionModel
    # 二进制方式来表示权限 0b 1111 1111 1111 1111 1111 1111 1111 1111
    # 最高权限
    DEVELOPMENT =       SUPER_PER
    # 1.基本权限
    GENERAL =           0b00000000000000000000000000000001
    # 2.管理产品权限
    PRODUCT =           0b00000000000000000000000000000010
    # 3.管理评论的权限
    # COMMENTER =         0b00000000000000000000000000000100
    # 4.管理板块、类型的权限
    BOARDER =           0b00000000000000000000000000001000
    # 5.管理用户的权限
    USER =              0b00000000000000000000000000010000
    # 6.系统设置的权限
    SETUP =             0b00000000000000000000000000100000

class HttpMethodEnumModel(enum.Enum):
    GET = "GET"         # 从服务器取资源
    POST = "POST"        # 在服务器新建资源
    PUT = "PUT"         # 在服务器更新资源（客户端提供改变后的完整资源）
    PATCH = "PATCH"       # 在服务器更新资源（客户端提供改变的数据）
    DELETE = "DELETE"      # 从服务器删除资源

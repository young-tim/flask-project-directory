#encoding:utf-8
# 用户模型

from apps.app import db
from apps.models.base import BaseModel
from apps.configs.db_config import DB_CONFIG
import shortuuid
from werkzeug.security import generate_password_hash, check_password_hash
from apps.configs.config import SUPER_PER
from apps.models.enums import GenderEnumModel, DomainEnumModel
from flask_login import UserMixin, current_user, AnonymousUserMixin
from apps.models.sys import SysUrlsModel
from apps.app import weblog


class UserPermissionModel(BaseModel):
    # ######### ！！暂不使用 ！！#########
    """
    权限集表

    角色权限关系：
        UserPermissionModel：存储每个页面/操作权限的内容与权限值（二进制）；
        UserRoleModel：角色的权限值是通过多个UserPermissionModel的权限值“|”计算得出；
        UserModel：用户可多选角色，角色权限值进行“|”计算；
    """
    # __tablename__ = DB_CONFIG['mysql']['prefix'] + 'user_permission'
    __table_args__ = {'comment': '权限集表'}  # 添加索引和表注释

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50), nullable=False, comment='权限编码', unique=True)
    value = db.Column(db.Integer, nullable=False, comment="权限值", unique=True)
    name = db.Column(db.String(100), default='', comment="权限名称")
    explain = db.Column(db.String(255), default='', comment="说明")
    is_default = db.Column(db.Integer, default=0, comment="是否默认拥有的权限：0 非默认；1 默认权限")

    @property
    def default_permission(self):
        default_permission = 0
        permissions = UserPermissionModel.query.all()
        for permission in permissions:
            if permission.is_default == 1:
                default_permission |= permission.value
        return default_permission

    @property
    def all_permission(self):
        return SUPER_PER


class UserRoleModel(BaseModel):
    # 用户角色表
    # __tablename__ = DB_CONFIG['mysql']['prefix'] + 'user_role'
    __table_args__ = {'comment': '用户角色表'}  # 添加索引和表注释

    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid, comment='唯一标识')
    code = db.Column(db.String(100), unique=False, comment='角色编码')
    name = db.Column(db.String(50), default='', comment='角色名称')
    desc = db.Column(db.String(100), default='', comment='角色介绍')
    domain = db.Column(db.Enum(DomainEnumModel), unique=False, comment='角色所属域')
    permissions = db.Column(db.Integer, default=UserPermissionModel.default_permission, comment='')

    is_default = db.Column(db.Integer, default=0, comment='默认角色：0 非默认，1 默认')
    status = db.Column(db.Integer, default=0, comment='状态：0 正常，-1 禁用')
    is_delete = db.Column(db.Integer, default=0, comment='是否删除：0 正常，1 表示已删除')

    def toDict(self):
        # 重载基类toDict方法
        c_dict = BaseModel.toDict(self)

        try:
            if "domain" in c_dict:
                # 枚举类型处理
                c_dict["domain_name"] = self.domain.name
                c_dict["domain_value"] = self.domain.value
                del c_dict["domain"]
        except Exception as e:
            weblog.err(e)

        return c_dict

    @property
    def role_info(self):
        info={
            # 'id': self.id,
            'name': self.name,
            'code': self.code,
            'domain': self.domain.name,
            'status': self.status
        }
        return info


# 用户-角色 关联表
role_to_user = db.Table(
    DB_CONFIG['mysql']['prefix'] + 'user_role_to_user',
    db.Column('role_id', db.String(100), db.ForeignKey('%s.id' % UserRoleModel.__tablename__), primary_key=True),
    db.Column('user_id', db.String(100), db.ForeignKey('%s.id' % (DB_CONFIG['mysql']['prefix'] + 'user')), primary_key=True)
)


class UserModel(BaseModel, UserMixin):
    # 用户信息表
    __tablename__ = DB_CONFIG['mysql']['prefix'] + 'user'
    __table_args__ = {'comment': '用户信息表'}  # 添加索引和表注释

    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid, comment='用户标识')
    username = db.Column(db.String(50), nullable=False, comment='用户名')
    telephone = db.Column(db.String(11), unique=False, default="", comment='手机号')
    _password = db.Column(db.String(100), nullable=False, comment='密码')
    email = db.Column(db.String(50), default="", comment='邮箱')
    avatar_url = db.Column(db.String(100), default="", comment='头像地址')
    signature = db.Column(db.String(100), default="", comment='个性签名')
    realname = db.Column(db.String(50), default="", comment='姓名')
    province_id = db.Column(db.Integer, default=0, comment='省份id')
    city_id = db.Column(db.Integer, default=0, comment='城市id')
    region_id = db.Column(db.Integer, default=0, comment='区域id')
    gender = db.Column(db.Enum(GenderEnumModel), default=GenderEnumModel.UNKNOW, comment='性别')
    superior_user_id = db.Column(db.String(100), nullable=True, default="", comment='上级用户id')
    login_error_num = db.Column(db.Integer, default=0, comment='登录错误次数，每次登录成功清零')
    last_login_time = db.Column(db.DateTime, comment='最后登录时间')

    status = db.Column(db.Integer, default=0, comment='状态：0 正常，-1 禁用')
    active = db.Column(db.Integer, default=1, comment='是否可用：0 不可用，1 表示可用')
    is_delete = db.Column(db.Integer, default=0, comment='是否删除：0 正常，1 表示已删除')

    # 上级用户
    # superior_user_id = db.Column(db.String(100), db.ForeignKey('%s.id' % UserModel.__tablename__), nullable=True, default="", comment='上级用户id')

    # 当上级用户有多个时，使用多对多的关系
    # superior_user = db.relationship('UserModel', secondary=superior_users, backref='users')
    # 当上级用户只有一个时，直接关联上级用户即可。自引用user.id，需加入remote_side参数
    # superior_user = db.relationship('UserModel', remote_side=[id])

    # 用户角色
    roles = db.relationship('UserRoleModel', secondary=role_to_user, backref='users')

    def __init__(self, user_id=None, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop("password")
        super(UserModel, self).__init__(*args, **kwargs)

    def toDict(self):
        # 重载基类toDict方法
        c_dict = BaseModel.toDict(self)

        try:
            roles = []
            for role in self.roles:
                roles.append(role.toDict())
            c_dict["roles"] = roles

            if "_password" in c_dict:
                del c_dict["_password"]
            if "gender" in c_dict:
                # 枚举类型处理
                c_dict["gender_name"] = self.gender.name
                c_dict["gender_value"] = self.gender.value
                del c_dict["gender"]
        except Exception as e:
            weblog.err(e)

        return c_dict

    @property
    def jwt_login_time_dict(self):
        """
        将jwt_login_time格式化为dict
        :return:
        """
        jwt_login_times = {}
        for v in self.jwt_login_time:
            jwt_login_times[v.id] = round(v.login_time / 1000000, 6)
        return jwt_login_times

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        # password赋值时，自动加密
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @property
    def permissions(self):
        """
        返回该用户的所有权限(值)
        :return: int permissions_value
        """
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions
        return all_permissions

    def can(self, permission):
        """
        has_permission：是否有权限
        :param permission: int 权限值
        :return:
        """
        # all_permissions = self.permissions
        # result = all_permissions & permission == permission
        # return result
        return self.permissions & permission == permission

    def page_permission_check(self, urls):
        """
        验证页面路由访问权限
        :param urls: 数组
        :return:
        """
        for url in urls:
            url_per = SysUrlsModel.query.filter_by(url=url.rstrip("/")).first()
            if url_per and url_per["type"] != "page" and "GET" in url_per["login_auth"]:
                custom_per = url_per["login_auth"]["GET"]
            if custom_per and current_user.can(custom_per):
                return True
            elif not custom_per:
                return True

    @property
    def is_developer(self):
        """
        是否是开发者。只要该用户拥有的权限位与最大权限位一致，则拥有开发者权限。
        :return: True or False
        """
        return self.has_permission(UserPermissionModel.all_permission)

    @property
    def user_info(self):
        info = {
            "name": self.realname,
            "status": self.status,
            "is_delete": self.is_delete,
            "email": self.email,
            "telephone": self.telephone,
            "avatar_url": self.avatar_url,
            "id": self.id
        }
        roles = []
        for role in self.roles:
            roles.append(role.role_info)
        info["roles"] = roles
        return info

    def __repr__(self):
        return '<User %r>' % (self.username)

# # 上级用户关联表，如有多个用户上级，则需要用该表
# superior_users = db.Table(
#     'bbx_superior_users',
#     db.Column('superior_user_id', db.String(100), db.ForeignKey('%s.id' % UserModel.__tablename__), primary_key=True),
#     db.Column('user_id', db.String(100), db.ForeignKey('%s.id' % UserModel.__tablename__), primary_key=True)
# )


class AnonymousUser(AnonymousUserMixin):
    # 匿名用户
    def __init__(self, **kwargs):
        super(AnonymousUser, self).__init__(**kwargs)

    @property
    def is_active(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return None


class UserJwtLoginTimeModel(BaseModel):
    # 用户JWT登录时间表
    # __tablename__ = DB_CONFIG['mysql']['prefix'] + 'user_jwt_login_time'
    __table_args__ = {'comment': '用户JWT登录时间表'}  # 添加索引和表注释

    id = db.Column(db.String(100), primary_key=True, comment='cid')
    user_id = db.Column(db.String(100), db.ForeignKey('%s.id' % UserModel.__tablename__), comment='用户ID')
    login_time = db.Column(db.BigInteger, comment='jwt登录时间')

    user = db.relationship('UserModel', backref='jwt_login_time')


class UserLoginLogModel(BaseModel):
    # 用户登录日志表
    # __tablename__ = DB_CONFIG['mysql']['prefix'] + 'user_login_log'
    __table_args__ = {'comment': '用户登录日志表'}  # 添加索引和表注释

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='唯一标识')
    user_id = db.Column(db.String(100), db.ForeignKey('%s.id' % UserModel.__tablename__), comment='用户ID')
    pass_error = db.Column(db.Integer, default=0, comment='登录结果：0 成功，1 失败')
    login_account = db.Column(db.String(100), default='', comment='登录账号')
    login_msg = db.Column(db.String(100), default='', comment='登录信息')
    ip = db.Column(db.String(20), default='', comment='登录IP')
    client = db.Column(db.String(100), default='', comment='客户端')

    user = db.relationship('UserModel', backref='login_log')

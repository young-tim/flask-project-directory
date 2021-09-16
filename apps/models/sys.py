#encoding:utf-8
from apps.app import db
from apps.models.base import BaseModel
from apps.models.enums import HttpMethodEnumModel


class SysTokenModel(BaseModel):
    # __tablename__ = DB_CONFIG['mysql']['prefix'] + 'sys_token'
    __table_args__ = {'comment': 'token表'}  # 添加索引和表注释

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='唯一标识')
    token_type = db.Column(db.String(50), default='', comment='token类型：secret_token')
    key = db.Column(db.String(1000), nullable=False, comment='')
    token = db.Column(db.String(1000), nullable=False, comment='')
    is_active = db.Column(db.Integer, default=1, comment='是否有效：1 有效，0 无效或停用')
    time = db.Column(db.Float, nullable=False, comment='生成时间戳')


class SysUrlsModel(BaseModel):
    # 站点url列表
    # __tablename__ = DB_CONFIG['mysql']['prefix'] + 'sys_urls'
    __table_args__ = {'comment': '站点url表'}  # 添加索引和表注释

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='唯一标识')
    endpoint = db.Column(db.String(255), default='', comment="服务端点")
    type = db.Column(db.String(100), nullable=False, comment="url类型，如api，page")
    url = db.Column(db.String(1000), default='', comment="url地址，无需带站点域名")
    login_auth = db.Column(db.Text, default='', comment="")


class SysUrlCustomPermissionModel(BaseModel):
    # url自定义权限
    # __tablename__ = DB_CONFIG['mysql']['prefix'] + 'sys_url_custom_permission'
    __table_args__ = {'comment': 'url自定义权限表'}  # 添加索引和表注释

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='唯一标识')
    url_id = db.Column(db.Integer, db.ForeignKey("%s.id" % SysUrlsModel.__tablename__), comment='url id')
    method = db.Column(db.Enum(HttpMethodEnumModel), default=HttpMethodEnumModel.GET, comment='http method')
    permission_value = db.Column(db.Integer, default=0, comment='自定义权限值')

    url = db.relationship('SysUrlsModel', backref='methods')


class SysCallRecordModel(BaseModel):
    # 系统调用记录
    # __tablename__ = DB_CONFIG['mysql']['prefix'] + 'sys_call_record'
    __table_args__ = {'comment': '系统调用记录表'}  # 添加索引和表注释

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='唯一标识')
    type = db.Column(db.String(50), comment='类型')
    req_path = db.Column(db.String(1000), default='', comment='请求路径')
    ip = db.Column(db.String(20), default='', comment='请求IP')
    user_id = db.Column(db.String(100), default='', comment='用户标识')


class SysSmsRecordModel(BaseModel):
    # 短信发送记录
    # __tablename__ = DB_CONFIG['mysql']['prefix'] + 'sys_sms_record'
    __table_args__ = {'comment': '短信发送记录表'}  # 添加索引和表注释

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='唯一标识')
    msg_type = db.Column(db.String(50), default='', comment='类型：验证码、短信通知、营销短信')
    content = db.Column(db.String(500), default='', comment='短信内容')
    telephone = db.Column(db.String(11), default='', comment='接收短信的手机号')
    # is_valid = db.Column(db.Integer, default=1, comment='是否有效：0 无效，1 有效')
    # is_sent = db.Column(db.Integer, default=0, comment='是否已发送：0 未发送，1 已发送')
    # send_at = db.Column(db.DateTime, comment='发送时间')
    # sent_at = db.Column(db.DateTime, comment='发送完成时间')
    biz_id = db.Column(db.String(50), default='', comment='阿里大鱼发送回执ID')
    code = db.Column(db.Integer, default=0, comment='发送结果编码')
    reason = db.Column(db.String(200), default='', comment='发送结果及原因')

    status = db.Column(db.Integer, default=1, comment='状态：1 发送正常，-1 发送失败')

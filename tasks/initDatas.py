import sys
sys.path.append("..")

from apps.app import db
from apps.models.enums import DomainEnumModel ,UserPersmissionEnumModel
from apps.models.sys import SysUrlsModel, SysUrlCustomPermissionModel, SysTokenModel
from apps.models.user import UserModel, UserPermissionModel, UserRoleModel
import time
"""
数据初始化函数
"""


class init_funs():

    def test(*args, **kwargs):
        print('init_funs')
        return 1, "ok"

    def init_role(*args, **kwargs):
        """
        初始化角色
        :param args:
        :param kwargs:
        :return:
        """
        # 访问者（可以修改个人信息）
        visitor = UserRoleModel(code='visitor', name='普通用户', desc='只能访问基础页面。', domain=DomainEnumModel.ADMIN, is_default=1)
        visitor.permissions = UserPersmissionEnumModel.GENERAL

        # 运营角色（修改个人信息，管理帖子，管理评论，管理前台用户）
        operator = UserRoleModel(code='operator', name='运营', desc='管理产品、板块。', domain=DomainEnumModel.ADMIN)
        operator.permissions = UserPersmissionEnumModel.GENERAL | UserPersmissionEnumModel.PRODUCT | UserPersmissionEnumModel.BOARDER

        # 管理员（拥有绝大部分权限）
        admin = UserRoleModel(code='admin', name='管理员', desc='拥有本系统大部分权限。', domain=DomainEnumModel.ADMIN)
        admin.permissions = UserPersmissionEnumModel.GENERAL | UserPersmissionEnumModel.PRODUCT | UserPersmissionEnumModel.BOARDER | UserPersmissionEnumModel.USER | UserPersmissionEnumModel.SETUP

        # 开发者（拥有系统全部功能）
        developer = UserRoleModel(code='developer', name='开发者', desc='超级管理员/开发人员专用角色。', domain=DomainEnumModel.ADMIN)
        developer.permissions = UserPersmissionEnumModel.DEVELOPMENT

        db.session.add_all([visitor, operator, admin, developer])
        db.session.commit()

        code = 0
        msg = "init role success"
        return code, msg


    def init_dev_user(*args, **kwargs):
        """
        初始化添加开发者用户
        :param args:
        :param kwargs:
        :return:
        """
        user = UserModel(username='developer', telephone='19999999999', password='dev123', email='developer@testß.com', realname='超级管理员')
        # 添加开发者角色
        role = UserRoleModel.query.filter_by(code='developer').first()
        if role:
            role.users.append(user)

        db.session.add(user)
        db.session.commit()

        code = 0
        msg = "init dev user success"
        return code, msg


    def init_test_users(*args, **kwargs):
        """
        添加一些测试用户
        :param args:
        :param kwargs:
        :return:
        """
        import random

        roles = ['visitor', 'operator']

        for i in range(25):
            name = 'test{}'.format(i + 1)
            phone = str(13300000000 + (i + 1))
            password = '123456'
            email = name + '@test.com'
            realname = '测试用户'
            role = random.choice(roles)
            user = UserModel(username=name, telephone=phone, password=password, email=email, realname=realname)
            # 添加开发者角色
            role = UserRoleModel.query.filter_by(code=role).first()
            if role:
                role.users.append(user)

            db.session.add(user)
            db.session.commit()

        code = 0
        msg = "init test users success"
        return code, msg


    # def init_permission(*args, **kwargs):
    #     """
    #     初始化添加权限列表
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     pers = [
    #         UserPermissionModel(code="general", value=0b00000000000000000000000000000001, name="访问权", explain="拥有基本的访问权限", is_default=1),
    #         UserPermissionModel(code="products", value=0b00000000000000000000000000000010, name="产品管理", explain="可对产品进行增删该查等操作权", is_default=0),
    #         UserPermissionModel(code="users", value=0b00000000000000000000000000000100, name="用户管理", explain="可对用户进行增删该查等操作权（但无法删除开发者账号）", is_default=0),
    #         UserPermissionModel(code="setup", value=0b00000000000000000000000000001000, name="设置", explain="系统设置、配置等权限", is_default=0),
    #         UserPermissionModel(code="development", value=0b1111111111111111111111111111111, name="开发权限", explain="可拥有系统最高权限,包含所有权限", is_default=0),
    #     ]
    #
    #     db.session.add_all(pers)
    #     db.session.commit()
    #
    #     code = 0
    #     msg = "init permission success"
    #     return code, msg



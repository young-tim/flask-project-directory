# -*-coding:utf-8-*-
from apps.app import db
from apps.models.user import UserModel
from apps.app import cache
from sqlalchemy import and_, or_


@cache.cached(timeout=7200, key_base64=False, db_type="redis")
def get_user(user_id=None, username=None, email=None, telephone=None):
    """
    获取一个user, 单条件过滤
    :param user_id:
    :return: user model obj
    """
    if user_id:
        q = [UserModel.id == user_id]
    elif username:
        q = [UserModel.username == username]
    elif email:
        q = [UserModel.email == email]
    elif telephone:
        q = [UserModel.telephone == telephone]
    else:
        return []
    # 拼接查询条件，并且排除已删除的用户
    q.append(UserModel.is_delete == 0)
    user = UserModel.query.filter(*q).order_by(UserModel.create_time.desc()).first()

    if user:
        # 将用户信息转为dict格式
        user = user.toDict()
        return user


def get_users_filter(username=None, email=None, telephone=None, op=None):
    """
    获取多个user, 多条件过滤
    :param username:
    :param email:
    :param telephone:
    :param op: 运算符：or
    :return: user model obj
    """
    # 拼接查询条件
    q = []
    or_q = []
    if username:
        if op == "or":
            or_q.append(UserModel.username == username)
        else:
            q.append(UserModel.username == username)
    if email:
        if op == "or":
            or_q.append(UserModel.email == email)
        else:
            q.append(UserModel.email == email)
    if telephone:
        if op == "or":
            or_q.append(UserModel.telephone == telephone)
        else:
            q.append(UserModel.telephone == telephone)

    # 拼接查询条件，并且排除已删除的用户
    q.append(UserModel.is_delete == 0)

    users = UserModel.query.filter(*q).filter(or_(*or_q)).order_by(UserModel.create_time.desc()).all()
    for i, k in enumerate(users):
        # 将返回的多条用户数据，格式为dict
        users[i] = k.toDict()
    if users:
        return users

def insert_user(data):
    """
    插入一条数据
    :param data:
    :return:
    """
    user = data
    db.session.add(user)
    db.session.commit()
    # 刷新并获取插入对象信息
    db.session.refresh(user)
    # 插入数据后的用户信息

    fun_name = "get_one_user"
    cache.delete_autokey(
        fun=fun_name,
        db_type="redis",
        username=user.username)
    cache.delete_autokey(fun=fun_name, db_type="redis", email=user.email)
    return user


def update_user(user_id, updata):
    """
    更新一个user
    :param user_id:
    :param updata: dict，需更新的数据
    :return: user model obj
    """
    r = UserModel.query.filter_by(id=user_id)
    r.update(updata)
    db.session.commit()

    user = r.first()
    clean_get_user_cache(user=user)
    return user


def delete_user(user_id):
    """
    delete user
    :param user_id:
    :return: user model obj
    """
    user = UserModel.query.get(user_id)
    if user:
        user.is_delete = 1
        db.session.commit()

    clean_get_user_cache(user=user)
    return user


def clean_get_user_cache(user_id=None, user=None):
    """
    清理get_one_user的cache
    :param user:
    :return:
    """
    fun_name = "get_one_user"
    if user_id and not user:
        user = UserModel.query.filter_by(id=user_id).first()
    if user:
        cache.delete_autokey(
            fun=fun_name,
            db_type="redis",
            user_id=user.id)
        cache.delete_autokey(
            fun=fun_name,
            db_type="redis",
            username=user.username)
        cache.delete_autokey(
            fun=fun_name,
            db_type="redis",
            email=user.email)
        cache.delete_autokey(
            fun=fun_name,
            db_type="redis",
            telephone=user.telephone)
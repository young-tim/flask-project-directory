#encoding: utf-8
import sys
sys.path.append("..")

from apps.app import app, db
from apps.core.db.database_config import MysqlConfig
from flask_script import Manager

manager = Manager(app)

app.config.from_object(MysqlConfig())
db.init_app(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

"""
处理计划任务、异步任务等
"""


@manager.option('-M', '--mode', dest='mode')
def schedule_tasks(mode=None):
    """
    定时任务脚本
    执行命令：
        python main.py schedule_tasks [-M <mode>]
    :param mode: all or funs name list(fun_name[,fun_name2,...])
    :return:
    """
    # 导入数据初始化脚本
    script = __import__('scheduleTasks')
    # 导入初始化函数对象
    script_funs = getattr(script, 'ScheduleTasks')

    funs = mode.split(',')
    try:
        for fun in funs:
            if fun[0] != '_':
                code, msg = getattr(script_funs, fun)()
                print("[code:{}] {}".format(code, msg))
    except Exception as e:
        print(e)


# ###################################################
# ################## 数据初始化命令 ##################
# ### 如果报日志错误，无需理会
@manager.option('-M', '--mode', dest='mode')
def init_datas(mode=None):
    """
    数据初始化，请尽量保证在首次运行站点时执行，切勿在运行中的站点执行该函数。
    执行命令：
        python main.py init_datas [-M <mode>]
    :param mode: all or funs name list(init_fun_name[,init_fun_name2,...])
    :return:
    """
    # 导入数据初始化脚本
    init_datas = __import__('initDatas')
    # 导入初始化函数对象
    init_funs = getattr(init_datas, 'init_funs')

    if mode == 'all' or mode is None:
        # 执行全部初始化函数，但执行顺序随机
        # funs = dir(init_funs)
        # 按顺序执行函数
        funs = [
            # 'init_permission',
            'init_role',
            'init_dev_user',
            'init_urls'
        ]
    else:
        # 执行传入的初始化函数名列表
        funs = mode.split(',')
    try:
        for fun in funs:
            if fun[0] != '_':
                code, msg = getattr(init_funs, fun)()
                print("[code:{}] {}".format(code, msg))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    manager.run()

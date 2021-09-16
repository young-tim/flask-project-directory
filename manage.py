#encoding:utf-8
import sys
import platform

# 启动网站
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps.app import app, db
from apps.core.flask.module_import import module_import
from apps.init_core_module import init_core_module
from apps.configs.config import MODULES

init_core_module(app)
module_import(MODULES)
manager = Manager(app)

# 使用Migrate绑定APP和db
migrate = Migrate(app, db)
# 添加数据库迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

# 判断操作系统
sysstr = platform.system()
if(sysstr !="Windows"):
    from signal import signal, SIGCHLD, SIG_IGN
    if not "--debug" in sys.argv and not "-D" in sys.argv:
        print(" * Signal:(SIGCHLD, SIG_IGN).Prevent child processes from becoming [Defunct processes].(Do not need to comment out)")
        signal(SIGCHLD, SIG_IGN)


# ###################################################
# ################ 数据库模型映射命令 ################
# ########## 仅在首次或数据库模型更新时使用 ##########
# 数据库模型初始化命令（仅首次需要。如果存在migrations目录，会无法初始化。）
# python manage.py db init
# 生成数据库模型迁移文件
# python manage.py db migrate
# 把模型映射到数据库中
# python manage.py db upgrade


if __name__ == '__main__':
    # 启动站点命令：
    # python manage.py runserver [--debug] [--host] [--port]
    manager.run()

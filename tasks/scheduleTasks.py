#encoding: utf-8
import sys
sys.path.append("..")

from apps.app import db

"""
计划任务
"""

class ScheduleTasks():
    def test(*args, **kwargs):
        print('init_funs')
        return 1, "ok"
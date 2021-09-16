#encoding:utf-8
import json
import sys
import regex as re
# from pymongo.cursor import Cursor


def ormobj_to_dict(obj):
    """
    将ORM的对象结果转为字典格式
    :param obj: ORM查询结果，且必须拥有"__table__"函数
                假如obj是list，则返回list字典集
                假如obj不是list，则直接返回字典数据
    :return: list_data or dict_data
    """
    if isinstance(obj, list):
        _data = []
        for data in obj:
            tmp = {}
            for column in data.__table__.columns:
                tmp[column.name] = str(getattr(data, column.name))
            _data.append(tmp)
        return _data
    else:
        _data = {}
        for column in obj.__table__.columns:
            _data[column.name] = str(getattr(obj, column.name))
        return _data


def objid_to_str(datas, fields=["_id"]):
    '''
    mongodb ObjectId to str
    :param datas:
    :param field:
    :return:
    '''
    if isinstance(datas, list):
        _datas = []
        for data in datas:
            for field in fields:
                data[field] = str(data[field])
            _datas.append(data)
        return _datas
    else:
        datas_keys = datas.keys()
        for field in fields:
            if field in datas_keys:
                datas[field] = str(datas[field])

        return datas


def json_to_pyseq(tjson):
    '''
    json to python sequencer
    :param json:
    :return:
    '''
    if tjson in [None, "None"]:
        return None
    elif not isinstance(tjson, (list, dict, tuple)) and tjson != "":
        if isinstance(tjson, (str, bytes)) and tjson[0] not in ["{", "[", "("]:
            return tjson
        try:
            tjson = json.loads(tjson)
        except:
            tjson = eval(tjson)
        else:
            if isinstance(tjson, str):
                tjson = eval(tjson)
    return tjson


def str_to_num(string, type=int):
    '''
    字符串转数字
    :param string: 字符串
    :param type: 转变方法(obj)
    :return:
    '''
    try:
        return type(string)
    except:
        if string:
            return 1
        elif not string or string.lower() == "false":
            return 0


class ConfDictToClass(object):
    """
    将配置文件中dict内容格式化为flask config可识别的格式
    """
    def __init__(self,config, key=None):
        if not isinstance(config, dict):
            print("[ERROR]:Must be a dictionary")
            sys.exit(-1)
        if key == "value":
            for k,v in config.items():
                if not re.search(r"^__.*__$", k):
                    self.__dict__[k] = v["value"]
        else:
            for k,v in config.items():
                self.__dict__[k] = v
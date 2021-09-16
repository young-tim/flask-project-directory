# -*-coding:utf-8-*-
from flask import url_for
from apps.configs.config import STATIC_PATH
from apps.configs.site_config import SITE_CONFIG


def get_localfile_path(file_url_obj):

    '''
    需要提供一个路径的对象
    :param file_url_obj:可以是站点的路径格式对象, 否则原对象返回
    :return:file url
    '''

    if isinstance(file_url_obj, dict) and "key" in file_url_obj:
        path = "{}/{}/{}".format(STATIC_PATH, SITE_CONFIG["upload"]["SAVE_DIR"], file_url_obj["key"]).replace("//", "/")
        return path
    else:
       return file_url_obj

def get_file_url(file_url_obj, save_dir=SITE_CONFIG["upload"]["SAVE_DIR"]):

    '''
    需要提供一个路径的对象
    :param file_url_obj:可以是站点的路径格式对象, 否则原对象返回
    :return:file url
    '''

    if isinstance(file_url_obj, dict) and "key" in file_url_obj:

        url = url_for('static', filename="{}/{}".format(save_dir, file_url_obj["key"]))

        return url
    elif isinstance(file_url_obj, str):
        return file_url_obj
    else:
        return None


def get_avatar_url(file_url_obj):
    '''
    专用于获取头像url
    :return:
    '''

    if "key" in file_url_obj and file_url_obj["key"]:
        return get_file_url(file_url_obj)
    elif "key" in file_url_obj and not file_url_obj["key"]:
        return SITE_CONFIG["account"]["DEFAULT_AVATAR"]
    return None
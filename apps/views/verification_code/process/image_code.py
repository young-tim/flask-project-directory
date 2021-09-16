# -*-coding:utf-8-*-
from apps.utils.verify.img_verify_code import create_img_code
from flask import request

def get_code():
    """
    获取图片验证码
    :return:
    """
    arg_width = int(request.argget.all('width', 0))
    arg_height = int(request.argget.all('height', 0))

    if (arg_width and arg_height):
        data = create_img_code(arg_width, arg_height)
    else:
        data = create_img_code()

    # 删除明文验证码
    del data['str']
    return data

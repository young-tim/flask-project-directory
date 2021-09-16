# -*-coding:utf-8-*-
import os
import random
from uuid import uuid1
import time
from apps.utils.upload.get_filepath import get_file_url
from apps.utils.upload.file_up import file_del, local_file_del
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from apps.configs.site_config import SITE_CONFIG
from apps.configs.config import FONT_PATH, FONT_TYPES, STATIC_PATH
from apps.app import cache, weblog
from apps.core.logger.web_logging import weblog


class CreateImgCode(object):

    def __init__(self, size_width, size_height, background):
        """
        初始化图片大小背景
        :param size_width:  图片大小宽
        :param size_height: 图片大小高
        :param background: 背景颜色
        """
        self.size = (size_width, size_height)
        self.background = background
        self.random_color = RandomColor()

    def create_pic(self):
        """
        创建一张图片
        """

        self.width, self.height = self.size
        self.img = Image.new("RGB", self.size, self.background)

        # 画笔
        self.draw = ImageDraw.Draw(self.img)

    def create_point(self, num):
        """
        画点
        :param num: 数量
        :return:
        """
        for i in range(num):
            self.draw.point(
                (random.randint(
                    0, self.width), random.randint(
                    0, self.height)), fill=self.random_color.random_color())

    def create_line(self, num):
        """
        画干扰线条
        :param num: 数量
        :return:
        """
        for i in range(num):
            self.draw.line(
                [
                    (random.randint(
                        0, self.width), random.randint(
                        0, self.height)), (random.randint(
                            0, self.width), random.randint(
                            0, self.height))], fill=self.random_color.random_color())

    def create_text(self, font_type, font_size, string):
        """
        把code画入图片
        :param font_type: 字体路径
        :param font_size: 字体大小
        :param string: 字符串
        :return:
        """

        font = ImageFont.truetype(font_type, font_size)
        str_list = list(string)
        # 横向边距
        w_margin = 4
        # 宽度字符间隔
        w_interval = (self.size[0] - w_margin * 2) / len(str_list)
        # 纵向边距
        h_margin = 4
        # 高度起点最低坐标

        h_scope = (self.size[1]-h_margin*2)-font_size
        for t, c in enumerate(str_list):
            h = random.randint(10, h_scope)
            self.draw.text((w_interval * t + 10, h), c,
                           font=font,
                           fill=self.random_color.random_color2())

    def istortion_shift(self):
        """
        给图片上的文字, 干扰线条再作扭曲, 移位等
        :return:
        """

        # self.img = self.img.transform(self.size, Image.PERSPECTIVE, (1,0, 0,0, 1,0 ,0,0),Image.BICUBIC)
        self.img = self.img.filter(ImageFilter.EDGE_ENHANCE_MORE)


class RandomColor:

    """
    验证码生成
    """

    def random_color(self):
        """
        随机生成字符颜色
        :return:
        """
        return (
            random.randint(
                64, 255), random.randint(
                64, 255), random.randint(
                64, 255))

    def random_color2(self):
        """
        随机生成用于干扰颜色
        :return:
        """
        return (
            random.randint(
                32, 180), random.randint(
                64, 180), random.randint(
                64, 180))


def random_char():
    """
    随机生成一个字母或数字字符
    :return:
    """

    i = random.randint(1, 3)
    if i == 1:
        an = random.randint(97, 122)
    elif i == 2:
        an = random.randint(65, 90)
    else:
        an = random.randint(48, 57)
    return chr(an)


def create_img_code(width=240, height=60, interference=0):
    """
    生成验证码图片
    width: 图片宽度，默认240
    height: 图片高度，默认60
    interference: 数值越高, 越难辨别,最小为10
    :return:
    """
    #  每次生成验证码的同时,我们删除本地过期验证码
    vercode_del(expiration_time=SITE_CONFIG["verify_code"]["EXPIRATION"])

    max_in = SITE_CONFIG["verify_code"]["MAX_IMG_CODE_INTERFERENCE"]
    min_in = SITE_CONFIG["verify_code"]["MIN_IMG_CODE_INTERFERENCE"]
    if interference < 10:

        if min_in < 10:
            min_in = 10
        if min_in > max_in:
            temp_max_in = max_in
            max_in = min_in
            min_in = temp_max_in
        else:
            min_in = 10
            max_in = 30
        interference = random.randint(min_in, max_in)

    # 验证码尺寸
    # width = 60 * 4
    # height = 60

    pic = CreateImgCode(width, height, 'white')
    pic.create_pic()
    pic.create_point(interference)
    pic.create_line(interference)

    # 随机生成字体路径
    font_path = FONT_PATH + random.choice(FONT_TYPES)

    # 生成随机码写入
    _str = ""
    for t in range(4):
        c = random_char()
        _str = "{}{}".format(_str, c)
    pic.create_text(font_path, 36, _str)

    # 扭曲
    pic.istortion_shift()

    # 保存路径
    local_dirname = SITE_CONFIG["verify_code"]["IMG_CODE_DIR"]
    save_dir = "{}/{}".format(STATIC_PATH, local_dirname).replace("//", "/")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    code_img = '{}__{}.jpg'.format(time.time(), uuid1())
    save_img = '{}/{}'.format(save_dir, code_img)

    # 保存
    pic.img.save(save_img, 'jpeg')



    code_url_info = {"key": code_img, "type": "local"}
    # 将文件名当做缓存key
    _cache_key = "verify_code_img_{}".format(code_url_info['key'])
    _code = {
        'url': code_url_info,
        'str': _str,
        'time': time.time(),
        "type": "image"}
    # 将图形验证码内容写入缓存
    cache.set(_cache_key, _code)

    _code['img_url_obj'] = _code['url']
    _code['url'] = get_file_url(code_url_info, save_dir=local_dirname)
    return _code


def verify_image_code(code_img_obj, code):
    """
    验证验证码
    :param code_img_obj:
    :param code:
    :return:
    """
    print(code_img_obj)
    r = False
    try:
        if not isinstance(code_img_obj, dict):
            code_img_obj = eval(code_img_obj)
    except Exception as e:
        err_msg = '''verify image code "code_img_obj" type error, not obj, dict or json type.
error code_img_obj:
{}'''.format(code_img_obj)
        weblog.error(err_msg)
        print(err_msg)
        return r

    if "key" not in code_img_obj:
        return r

    expiration_time = SITE_CONFIG["verify_code"]["EXPIRATION"]
    _cache_key = "verify_code_img_{}".format(code_img_obj['key'])
    code_data = cache.get(_cache_key)
    if code_data:
        if code.lower() == code_data['str'].lower(
        ) and time.time() - code_data['time'] < expiration_time:
            vercode_del(file_url_obj=code_data['url'])
            r = True
    return r


def vercode_del(file_url_obj=None, expiration_time=None):
    """
    删验证码
    :param url:
    :param expiration_time:顺便删除过期的验证码
    :return:
    """

    if file_url_obj:
        file_path = "{}/{}/{}".format(STATIC_PATH, SITE_CONFIG['verify_code']['IMG_CODE_DIR'], file_url_obj["key"]).replace("//", "/")
        local_file_del(file_path)
        cache.delete("verify_code_img_{}".format(file_url_obj["key"]))

    if expiration_time:
        # 删除过期的验证码，只删除了本地的，没有删除缓存里的验证码（但缓存验证码过期后自动删除）
        local_dirname = SITE_CONFIG["verify_code"]["IMG_CODE_DIR"]
        local_file_dir = "{}/{}".format(STATIC_PATH, local_dirname).replace("//", "/")
        local_file_del(path=local_file_dir, expiration_time=expiration_time)
# -*-coding:utf-8-*-
import os

import time
from flask import render_template, url_for
from apps.core.blueprint import main, static
from apps.core.template.template import render_absolute_path_template
from apps.configs.site_config import SITE_CONFIG
from apps.utils.format.time_format import time_to_utcdate


def get_email_html(data):
    """
    获取发送邮件使用的html模板
    :param data: 需要再模板中使用的数据, 使用Jinjia2
            格式:{"title": "标题",
                "body": "正文, 可以使用html标签",
                "other_info":"其他信息, 可以使用html标签",
                }
    :return:
    """

    # 查找邮件发送html模板
    data["app_name"] = SITE_CONFIG["site_info"]["APP_NAME"]
    data["app_logo_url"] = SITE_CONFIG["site_info"]["LOGO_IMG_URL"]
    conf_site_url = SITE_CONFIG["site_info"]["SITE_URL"]
    if conf_site_url:
        data["site_url"] = url_for(conf_site_url)
    else:
        data["site_url"] = url_for("index")
    data["utc_time"] = time_to_utcdate(
        time_stamp=time.time(),
        tformat="%Y-%m-%d %H:%M:%S")

    path = "email/send-temp.html"
    absolute_path = os.path.abspath(
        "{}/{}".format(static.template_folder, path))

    html = render_template(path, data=data)

    return html

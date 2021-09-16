# -*-coding:utf-8-*-
import time
from apps.app import db, alidayu
from apps.models.sys import SysSmsRecordModel


def send_sms(numbers, **kwargs):
    """
    短信发送
    :param numbers: 支持多个电话号码，用英文","分割。
    :param **kwargs: 根据短信模板分别传入字段数据。
    :return:
    """

    sms_res = alidayu.send_sms(telephone=numbers, **kwargs)
    if sms_res['Code'] == 'OK':
        status = 1
        result = (True, '短信发送成功')
    else:
        status = -1
        result = (False, '短信发送失败')

    sms_log = SysSmsRecordModel(msg_type='验证码',
                                content='',
                                telephone=numbers,
                                code=sms_res['Code'],
                                reason=sms_res['Message'],
                                status=status
                                )
    db.session.add(sms_log)
    db.session.commit()

    return result

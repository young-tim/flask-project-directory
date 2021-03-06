#encoding:utf-8
import json
import time
import os
from flask_mail import Message
from apps.utils.async.async import async_process
from apps.app import mail, app

def send_email(subject, recipients, text_msg=None, html_msg=None, attach=None,
               send_independently=False):
    '''
    发送email
    :param subject:邮件主题
    :param recipients:收件人，数组类型
    :param text_msg:文本信息
    :param html_msg:html信息
    :param attach:(<filename>,<content_type>) 附件
    :param send_independently:如果为True, 独立给recipients中的每个地址发送信息,
            否则,一次发送, 收件人能看到其他收件人的邮箱

    :return:
    '''

    msg = Message(subject=subject,
                  sender=app.config.get("MAIL_DEFAULT_SENDER"))
    if html_msg:
        msg.html = html_msg
    elif text_msg:
        msg.body = text_msg
    if attach and len(attach) == 2:
        with app.open_resource(attach[0]) as fp:
            msg.attach(os.path.split(attach[0])[-1], attach[1], fp.read())

    # send email
    send_async_email(app, msg,
                     recipients=recipients,
                     send_independently=send_independently)

@async_process
def send_async_email(app, msg, recipients, send_independently=False):
    '''
    异步发送email
    :param app:
    :param msg:
    :param send_independently: 每个单独发送
    :return:
    '''
    # mdb_sys.init_app(reinit=True)
    with app.app_context():
        if send_independently:
            # 独立发送, 先连接好邮件服务器
            with mail.connect() as conn:
                for recipient in recipients:
                    msg.recipients = [recipient]
                    send_email_process(msg, conn)
        else:
            msg.recipients = recipients
            return send_email_process(msg)


def send_email_process(msg, connected_instance=None):
    '''
    发送
    :param msg:
    :param connected_instance: 已连接的实例
    :return:
    '''
    error_info = None
    try:
        if connected_instance:
            r = connected_instance.send(msg)
        else:
            r = mail.send(msg)
        if not r:
            status = "normal"
        else:
            status = "abnormal"
    except Exception as e:
        error_info = json.dumps(str(e))
        status = "error"

    log = {
        "type":"email",
        "error_info": error_info,
        'status': status,
        'subject': msg.subject,
        'from': msg.sender,
        'to': list(msg.send_to),
        'date': msg.date,
        'body': msg.body,
        'html': msg.html,
        'msgid': msg.msgId,
        'time': time.time()
    }
    # mdb_sys.db.sys_message.insert_one(log)
    if not status:
        return 0
    else:
        return -1
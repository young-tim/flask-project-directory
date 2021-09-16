#encoding:utf-8
import regex as re
import time
import datetime

def time_to_utcdate(time_stamp=None, tformat = "%Y%m%d"):
    '''
    Timestamp to UTC date
    :param time_stamp:
    :param tformat:
    :return:
    '''
    # If the default parameters in parameters using time, Time will not change
    if not time_stamp:
        time_stamp=time.time()
    utcdate = datetime.datetime.utcfromtimestamp(time_stamp).strftime(tformat)
    if utcdate.isdigit():
        return int(utcdate)
    else:
        return utcdate

def date_to_time(date, tformat = "%Y%m%d"):
    '''
    Date to Timestamp
    :param date:
    :param tformat:
    :return:
    '''
    utc = time.mktime(datetime.datetime.utcnow().timetuple())
    local = time.mktime(datetime.datetime.now().timetuple())
    jet_lag = (local-utc)//3600
    if not isinstance(date, str):
        date = str(int(date))
    time_stamp = time.mktime(datetime.datetime.strptime(date, tformat).timetuple())
    time_stamp += 3600*jet_lag
    return time_stamp


# #############


def timestamp_to_strtime(timestamp, time_accuracy='ms'):
    """将整数的毫秒时间戳转化成本地普通时间 (字符串格式)
    :param timestamp: 整数的毫秒时间戳 (1456402864242)
    :param time_accuracy: 时间精度：ms 毫秒，s 秒
    :return: 返回字符串格式 {str}'2016-02-25 20:21:04.242000'
    """
    if time_accuracy=='ms':
        local_str_time = datetime.datetime.fromtimestamp(timestamp / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
    else:
        local_str_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return local_str_time

def timestamp_to_datetime(timestamp, time_accuracy='ms'):
    """将整数的毫秒时间戳转化成本地普通时间 (datetime 格式)
    :param timestamp: 整数的毫秒时间戳 (1456402864242)
    :param time_accuracy: 时间精度：ms 毫秒，s 秒
    :return: 返回 datetime 格式 {datetime}2016-02-25 20:21:04.242000
    """
    if time_accuracy == 'ms':
        local_dt_time = datetime.datetime.fromtimestamp(timestamp / 1000.0)
    else:
        local_dt_time = datetime.datetime.fromtimestamp(timestamp)
    return local_dt_time

def datetime_to_strtime(datetime_obj, time_accuracy='ms'):
    """将 datetime 格式的时间 (含毫秒) 转为字符串格式
    :param datetime_obj: {datetime}2016-02-25 20:21:04.242000
    :param time_accuracy: 时间精度：ms 毫秒，s 秒
    :return: {str}'2016-02-25 20:21:04.242'
    """
    if time_accuracy == 'ms':
        local_str_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
    else:
        local_str_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    return local_str_time

def datetime_to_timestamp(datetime_obj, time_accuracy='ms'):
    """将本地(local) datetime 格式的时间 (含毫秒) 转为时间戳
    :param datetime_obj: {datetime}2016-02-25 20:21:04.242000
    :param time_accuracy: 时间精度：ms 毫秒，s 秒
    :return: 时间戳  1456402864242
    """
    if time_accuracy=='ms':
        local_timestamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
    else:
        local_timestamp = int(time.mktime(datetime_obj.timetuple()) + datetime_obj.microsecond)
    return local_timestamp

def strtime_to_datetime(timestr, time_accuracy='ms'):
    """将字符串格式的时间 (含毫秒) 转为 datetiem 格式
    :param timestr: {str}'2016-02-25 20:21:04.242'
    :param time_accuracy: 时间精度：ms 毫秒，s 秒
    :return: {datetime}2016-02-25 20:21:04.242000
    """
    if time_accuracy == 'ms':
        local_datetime = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
    else:
        local_datetime = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    return local_datetime

def strtime_to_timestamp(local_timestr, time_accuracy='ms'):
    """将本地时间 (字符串格式，含毫秒) 转为整数的毫秒时间戳
    :param local_timestr: {str}'2016-02-25 20:21:04.242'
    :param time_accuracy: 时间精度：ms 毫秒，s 秒
    :return: 1456402864242
    """
    local_datetime = strtime_to_datetime(local_timestr, time_accuracy)
    timestamp = datetime_to_timestamp(local_datetime, time_accuracy)
    return timestamp

def current_datetime(time_accuracy='ms'):
    """返回本地当前时间, 包含datetime 格式, 字符串格式, 时间戳格式
    :param time_accuracy: 时间精度：ms 毫秒，s 秒
    :return: (datetime 格式, 字符串格式, 时间戳格式)
    """
    # 当前时间：datetime 格式
    if time_accuracy=="ms":
        local_datetime_now = datetime.datetime.now()
    else:
        local_datetime_now = datetime.datetime.now().replace(microsecond=0)
    # 当前时间：字符串格式
    local_strtime_now = datetime_to_strtime(local_datetime_now, time_accuracy)
    # 当前时间：时间戳格式 整数，毫秒
    local_timestamp_now = datetime_to_timestamp(local_datetime_now, time_accuracy)
    return local_datetime_now, local_strtime_now, local_timestamp_now


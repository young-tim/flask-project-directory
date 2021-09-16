#encoding:utf-8
from multiprocessing import Process
import threading

'''
decorators
'''

def async_thread(f):
    '''
    threading Thread
    多线程
    :param f:
    :return:
    '''
    def wrapper(*args, **kwargs):
        t =threading.Thread(target=f,args=args, kwargs = kwargs)
        t.start()
    return wrapper

def async_process(f):
    '''
    multiprocessing Process
    多进程
    暂不支持windows
    :param f:
    :return:
    '''
    def wrapper(*args, **kwargs):
        p = Process(target=f, args=args, kwargs=kwargs)
        p.start()
    return wrapper

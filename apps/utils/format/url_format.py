#encoding:utf-8
from tld import get_tld


def get_domain(url):
    '''
    获取url中的全域名
    :param url:
    :return:
    '''
    res = get_tld(url, as_object=True)
    return "{}.{}".format(res.subdomain, res.tld)
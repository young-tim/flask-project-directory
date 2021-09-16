#encoding:utf-8
from flask import Response, jsonify


class Response(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(Response, cls).force_type(rv, environ)


def response_format(data, code=200):
    '''
    :param data:
    :param code:http code
    :return:
    '''
    if not isinstance(data, dict):
        return data, code
    if "code" not in data.keys():
        return data, code
    return data, data["code"]

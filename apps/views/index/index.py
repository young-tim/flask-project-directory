#encoding:utf-8
from apps.core.blueprint import main
from apps.core.flask.restful import succcess

@main.route('/')
def index():
    data = {
        "code": 200,
        "msg": "OK",
        "data": None
    }
    return succcess(data)

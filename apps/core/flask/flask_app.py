#encoding:utf-8
from flask import Flask
from apps.core.flask.response import Response

class App(Flask):
    response_class = Response
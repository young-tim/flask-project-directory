#encoding:utf-8
from importlib import import_module

def module_import(modules):

    for module in modules:
        import_module(module)
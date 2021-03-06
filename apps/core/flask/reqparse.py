# -*-coding:utf-8-*-
import regex as re


class ArgVerify():

    def required(self, **kwargs):
        for reqarg in kwargs.get("reqargs"):
            if not reqarg[1]:
                data = {'msg': 'The "{}" cannot be empty'.format(reqarg[0]),
                        'msg_type': "w", "code": 422}
                return False, data
        return True, None

    def min_len(self, **kwargs):

        vr = kwargs.get("vr")
        for reqarg in kwargs.get("reqargs"):
            if len(reqarg[1]) < vr:
                data = {'msg': 'The minimum length of "{}" is {} characters'.format(reqarg[0], vr),
                        'msg_type': "w", "code": 422}
                return False, data
        return True, None


    def max_len(self, **kwargs):

        vr = kwargs.get("vr")
        for reqarg in kwargs.get("reqargs"):
            if len(reqarg[1]) > vr:
                data = {'msg': 'The maximum length of "{}" is {} characters'.format(reqarg[0], vr),
                        'msg_type': "w", "code": 422}
                return False, data
        return True, None

    def need_type(self, **kwargs):

        vr = kwargs.get("vr")
        for reqarg in kwargs.get("reqargs"):
            if not isinstance(reqarg[1], vr):
                data = {'msg': '"{}" needs to be of type {}'.format(reqarg[0], vr.__name__),
                        'msg_type': "w", "code": 422}
                return False, data
        return True, None

    def only(self, **kwargs):
        vr = kwargs.get("vr")
        for reqarg in kwargs.get("reqargs"):
            if not reqarg[1] in kwargs.get("vr"):
                data = {'msg': 'The value of parameter "{}" can only be one of "{}"'.format(reqarg[0], ",".join(vr)),
                        'msg_type': "w", "code": 422}
                return False, data
        return True, None

    def can_not(self, **kwargs):
        vr = kwargs.get("vr")
        for reqarg in kwargs.get("reqargs"):
            if reqarg[1] in vr:
                data = {'msg': 'The value of parameter "{}" can not be "{}"'.format(reqarg[0], ",".join(vr)),
                        'msg_type': "w", "code": 422}
                return False, data
        return True, None

    def allowed_type(self, **kwargs):
        vr = kwargs.get("vr")
        for reqarg in kwargs.get("reqargs"):
            if type(reqarg[1]) not in vr:
                data = {'msg': 'Parameter {} can only be of the following type: "{}"'.format(reqarg[0], ",".join(vr)),
                        'msg_type': 'error', "code": 422}
                return False, data
        return True, None

    def regex_rule(self,**kwargs):

        vr = kwargs.get("vr")
        if vr["is_match"]:
            for reqarg in kwargs.get("reqargs"):
                if not re.search(vr["rule"], reqarg[1]):
                    return False, {'msg': 'The value of parameter "{}" is illegal'.format(reqarg[0]),
                            'msg_type': "w", "code": 422}

        else:
            for reqarg in kwargs.get("reqargs"):
                if re.search(vr["rule"], reqarg[1]):
                    return False, {'msg': 'The value of parameter "{}" is illegal'.format(reqarg[0]),
                            'msg_type': "w", "code": 422}


        return True, None

arg_ver = ArgVerify()
def arg_verify(reqargs=[],  **kwargs):

    '''
    :param reqargs:???????????????[(arg_key, arg_value)]
    :param required:bool,  ???True??????????????????
    :param min_len: int, ????????????
    :param max_len: int, ????????????
    :param need_type: ?????????int, dict, list .tuple
    :param only: ??????, ?????????only??????????????????
    :param can_not: ??????, ?????????can_not????????????
    :param allowed_type: ??????, ????????????????????????allowed_type????????????
    :param regex_rule: Such as::{"rule":r".*", "is_match":True}
                        is_match ???True ????????????????????????, False ?????????????????????????????????
    :param args:
    :param kwargs:
    :return:????????????,????????????
    '''
    for k,v in kwargs.items():
        s,r = getattr(arg_ver, k)(reqargs=reqargs, vr=v)
        if not s:
            return s,r
    return True, None

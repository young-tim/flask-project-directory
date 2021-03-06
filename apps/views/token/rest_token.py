# -*-coding:utf-8-*-
from flask import request
from apps.core.flask.login_manager import login_required
from apps.configs.config import METHOD_WARNING
from apps.core.blueprint import api
from apps.core.flask.permission import permission_required
from apps.core.flask.response import response_format
from apps.views.token.process.rest_token import get_secret_token, create_secret_token, \
    activate_secret_token, disable_secret_token, delete_secret_token, rest_token_auth



@api.route('/token/access-token', methods=['GET'])
@permission_required(use_default=False)
def api_access_token():
    '''获取access-token
    @@@

    #### args
    - RestToken: [String], "SecretToken <token/key>"
    - ClientId: [String], 可选，有则使用客户端提供的ClientId, 否则创建新的ClientId

    #### return
    ``` json
    {
        "access_token": "ZjhkNGNmNTgtNTYwZS0xMWVhLWIwMDEtYWNiYzMyYmE3NWFmODc4Nzgx",
        "client_id": "sys_session_rest-f8bebb1e-560e-11ea-bd10-acbc32ba75af"
    }
    ```

    #### desc
    - 客户端获取/刷新AccessToken (必须使用SecretToken验证通过).
    - 如果请求头中带有ClientId 则使用客户端提供的ClientId, 否则创建新的ClientId

    @@@
    '''

    data = rest_token_auth.create_access_token()
    return response_format(data)


@api.route('/admin/token/secret-token', methods=['GET', 'POST', 'PUT','DELETE'])
@login_required
@permission_required()
def api_rest_token():
    '''
    @@@
    - GET: 获取所有secret token

    - POST: 创建一个secret token

    - PUT: 激活或禁用一个id
        - token_id: [id], token id.
        - action: [string], 如果为"activate"则激活token, 为"disable"禁用token.

    - DELETE: 删除一个token
        - token_id: [id], token id.

    #### desc
    客户端访问使用的secret token管理

    @@@
    '''

    if request.c_method == "GET":
        data = get_secret_token()

    elif request.c_method == "POST":
        data = create_secret_token()

    elif request.c_method == "PUT":
        if request.argget.all("action") == "activate":
            data = activate_secret_token()
        else:
            data = disable_secret_token()

    elif request.c_method == "DELETE":
        data = delete_secret_token()
    else:
        data = {"msg_type": "w", "msg": METHOD_WARNING, "code": 405}
    return response_format(data)


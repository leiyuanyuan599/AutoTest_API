#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project   : 
@File      : jt_login.py
@Time      : 2025/10/24 16:31
@Author    : LeiYuanyuan
@Desc      :
"""

import json
from common.BaseRequest import BaseRequest
from common.crypto_utils import decode_base64


def jt_login(appid, jtUuid, mobile):
    param_dict = {
        "jtUuid": jtUuid,
        "mobile": mobile,
        "centerNo": "CN001",
        "branchNo": "BRN001",
        "timestamp": "1"
    }
    payload = {
        "appId": f"{appid}",
        "sign": "unlock-dev",
        "aesKey": "unlock-dev",
        "param": json.dumps(param_dict, separators=(',', ':'))
    }
    jt_login_url = BaseRequest(appname='BluePayManage1')
    resp_json = jt_login_url.send(method='post', url='open-api/jt/wallet/loginToken', payload=payload)

    if resp_json.get("code") == 10000:
        authUrl = resp_json["data"]["authUrl"]
        token = resp_json["data"]["token"].strip()
        uuid = resp_json["data"]["uuid"]
        return authUrl, decode_base64(token), uuid,
    else:
        print(f"登录失败，业务码：{resp_json.get('code')}，信息：{resp_json.get('message')}")
        return None


if __name__ == '__main__':
    appid = '4b585c9e8ad7462ab28b2c8cd73bc06c'
    jtUuid = 'uuu098711675341'
    mobile = '0659901248'
    token = jt_login(appid, jtUuid, mobile)[1]

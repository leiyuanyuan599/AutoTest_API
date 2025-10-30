#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project   : 
@File      : getAgentMerchantList.py
@Time      : 2025/10/29 18:04
@Author    : LeiYuanyuan
@Desc      : 获取代理商户列表（DB管理）
"""
from common.BaseRequest import BaseRequest


class GetAgentMerchantList():
    appname = 'BluePayManage1'
    method  = 'post'
    url     = '/manager_api/merchantManagement/merchant/getAgentMerchantList'
    headers = {"content-type": "application/json"}
    body    = {
        "audit_status": 4,
        "audit_step": 2
    }


if __name__ == '__main__':
    agent_api = GetAgentMerchantList()
    # req = BaseRequest(appname='BluePayManage1')
    req = BaseRequest(appname=agent_api.appname)
    res = req.send(method=agent_api.method, url=agent_api.url, payload=agent_api.body)

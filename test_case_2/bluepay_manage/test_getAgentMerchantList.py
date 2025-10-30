#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project   : 
@File      : test_getAgentMerchantList.py
@Time      : 2025/10/29 18:45
@Author    : LeiYuanyuan
@Desc      :
"""
from common.BaseRequest import BaseRequest
from api.manager_api import getAgentMerchantList


class TestGetAgentMerchantList:
    def test_001(self):
        api_cls = getAgentMerchantList.GetAgentMerchantList()
        req = BaseRequest(appname=api_cls.appname)
        res = req.send(method=api_cls.method,
                       url=api_cls.url,
                       payload=api_cls.body)
        print(res)
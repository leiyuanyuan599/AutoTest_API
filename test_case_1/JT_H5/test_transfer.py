#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project   : 
@File      : test_transfer.py
@Time      : 2025/10/29 17:25
@Author    : LeiYuanyuan
@Desc      :
"""
import pytest, allure
from common.engine import FlowRunner


@allure.epic("JT_Transfer")
def test_fund_list_inherit(default_req):
    runner = FlowRunner(default_req)
    runner.run("data/yaml/login.yaml")
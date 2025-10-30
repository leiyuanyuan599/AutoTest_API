#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project   : 
@File      : test_fund_purchase.py.py
@Time      : 2025/10/13 18:10
@Author    : LeiYuanyuan
@Desc      :
"""
import pytest, allure
from common.engine import FlowRunner


@allure.epic("跨目录继承payload流程")
def test_fund_list_inherit():
    runner = FlowRunner()
    runner.run("data/flow/fund_purchase_flow.yml")  # 不传入路径则是data中与testcase路径一致的文件，没有就报错

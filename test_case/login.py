#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project   : 
@File      : login.py
@Time      : 2025/10/13 17:58
@Author    : LeiYuanyuan
@Desc      :
"""
import pytest, allure
from common.engine import FlowRunner


@allure.epic("JT_login")
def test_fund_list_inherit():
    runner = FlowRunner()
    runner.run("data/yaml/login.yaml")
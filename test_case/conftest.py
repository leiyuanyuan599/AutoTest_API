#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project   : 
@File      : conftest.py.py
@Time      : 2025/10/13 17:57
@Author    : LeiYuanyuan
@Desc      :
"""
import os
import pytest
import allure
import json
from common.settings import base_url, load_yaml
from common.BaseRequest import BaseRequest


# ---------------- 全局单例（无加密、无用户） ----------------
@pytest.fixture(scope="session")
def default_req():
    """单接口/无加密场景直接用它"""
    return BaseRequest(token=None)


# ---------------- 多应用-多用户-加密池（按需拿） ----------------
def _user_pool():
    return load_yaml("config/key_pool.yml")["app"]


@pytest.fixture(scope="session")
def user_req(request):
    """
    用法：
        @pytest.mark.parametrize("app,user", [("fund-admin","admin"),("fund-client","c-user")])
        def test_cross(app, user, user_req):
            req = user_req(app, user)
    """

    def _make(app: str, user: str):
        cfg = _user_pool()[app]["users"][user]
        enc = cfg["encrypt"]
        return BaseRequest(
            base_url=base_url(app),
            encrypt_type=enc["type"],
            key=bytes.fromhex(enc["key"]),
            iv=bytes.fromhex(enc["iv"]) if enc.get("iv") else None,
            token=None,  # token 在流程里再刷新
        )

    return _make


# ---------------- 自动 data 路径映射（FlowRunner 用） ----------------
@pytest.fixture(scope="session")
def data_path(request):
    """
    将当前测试文件路径映射到 data/ 同名 .yml
    例：test_cases/flow/test_demo.py  -> data/flow/test_demo.yml
    """
    test_file = request.node.fspath
    rel = os.path.relpath(test_file, os.path.join(os.path.dirname(__file__)))
    rel = rel.replace(".py", ".yml")
    return os.path.join("data", rel)


# ---------------- Allure 失败截图 & 日志落盘 ----------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        # 把最后请求/响应写进 Allure
        if hasattr(item.instance, "last_resp"):
            allure.attach(
                json.dumps(item.instance.last_resp, ensure_ascii=False, indent=2),
                name="失败响应",
                attachment_type=allure.attachment_type.JSON
            )

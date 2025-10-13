#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project   : 
@File      : engine.py.py
@Time      : 2025/10/13 18:19
@Author    : LeiYuanyuan
@Desc      : 跨应用、跨用户、多加密配置  流程引擎
"""
import functools
import json
import os
import re
import inspect
from jsonpath import jsonpath
from common.BaseRequest import BaseRequest
from common.settings import base_url, load_yaml

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))   # common 的上级


# 加载钥匙池（只一次）
@functools.lru_cache(maxsize=1)
def _key_pool():
    return load_yaml("config/key_pool.yml")["app"]


def _abs_path(self, rel: str) -> str:
    """相对项目根 -> 绝对路径"""
    return os.path.join(PROJECT_ROOT, rel.replace("/", os.sep))


def _merge_payload(self, step: dict) -> dict:
    base = {}
    if step.get("base_payload_file"):
        with open(self._abs_path(step["base_payload_file"]), encoding="utf-8") as f:
            base = json.load(f)
    delta = {}
    if step.get("payload_delta"):
        delta = json.loads(step["payload_delta"])
    return {**base, **delta}


class FlowRunner:
    def __init__(self, flow_file=None):
        # 未传路径时，用调用者文件路径映射到 data/
        if flow_file is None:
            caller_file = inspect.stack()[1].filename          # 谁 new 的我
            rel = os.path.relpath(caller_file, os.path.join(os.path.dirname(__file__), '..', 'test_cases'))
            rel = re.sub(r'\.py$', '.yml', rel)                # test_xxx.py → test_xxx.yml
            flow_file = os.path.join('data', rel)
        self.flow_file = flow_file
        self.vars = {}
        self.reqs = {}

    # ---------- 对外唯一入口 ----------
    def run(self, flow_file):
        flow = load_yaml(flow_file)
        self.vars.update(os.environ)  # 允许 ${ENV} 变量
        for step in flow["steps"]:
            self._run_step(step)

    # ---------- 单 step 执行 ----------
    def _run_step(self, step):
        # 1. 变量替换  ${xxx}
        tpl = json.dumps(step, ensure_ascii=False)
        tpl = re.sub(r'\$\{(\w+)\}', lambda m: str(self.vars.get(m.group(1), m.group(0))), tpl)
        step = json.loads(tpl)

        # 2. 获取对应 BaseRequest
        req = self._get_req(step["app"], step["user"])

        # 3. 发请求
        resp = req.send(
            method=step["method"],
            url=step["url"],
            payload=step.get("payload"),
            headers=step.get("headers", {})
        )

        # 4. 提取
        for name, path in step.get("extract", {}).items():
            self.vars[name] = jsonpath(resp, path)[0]

        # 5. 断言
        for rule in step.get("assert", []):
            left_expr, right_val = rule.split("==", 1)
            left = jsonpath(resp, left_expr.strip())[0]
            right = eval(right_val.strip())  # 支持数字、字符串、布尔
            assert left == right, f"{left_expr} 实际值 {left} 不等于期望 {right}"

    # ---------- 工厂：拿 (app,user) 级别的 BaseRequest ----------
    def _get_req(self, app: str, user: str):
        cache_key = (app, user)
        if cache_key not in self.reqs:
            cfg = _key_pool()[app]["users"][user]  # 两级查找
            token = self.vars.get(f"{user}Token")  # 前面 extract 的 token
            enc = cfg["encrypt"]
            self.reqs[cache_key] = BaseRequest(
                base_url=base_url(app),
                token=token,
                encrypt_type=enc["type"],
                key=bytes.fromhex(enc["key"]),
                iv=bytes.fromhex(enc["iv"]) if enc.get("iv") else None
            )
        return self.reqs[cache_key]

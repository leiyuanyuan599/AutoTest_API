#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project   : 
@File      : settings.py.py
@Time      : 2025/10/13 17:19
@Author    : LeiYuanyuan
@Desc      :
"""
import functools
import os
import yaml

# --------- 通用 yaml 加载 ---------
def load_yaml(file_name: str):
    """相对项目根目录读取 yaml"""
    path = os.path.join(os.path.dirname(__file__), '..', file_name)
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)


# --------- 应用域名 ----------
@functools.lru_cache(maxsize=None)
def _cfg():
    return load_yaml("config/sit.yaml")


def base_url(app: str) -> str:
    node = _cfg()["app"][app]
    host = node["host"]
    port = node["port"]
    return f"https://{host}:{port}"


# ===== 2. 数据库 =====
def db_conf(db='order'):
    return _cfg()['db'][db]


# ===== 3. Redis =====
def redis_conf(name='cache'):
    return _cfg()['redis'][name]

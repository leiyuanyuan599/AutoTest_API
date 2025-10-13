#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project   : 
@File      : read_data.py
@Time      : 2025/10/13 15:23
@Author    : LeiYuanyuan
@Desc      :
"""

import json
import os
import yaml


def load_yaml(file_name):
    path = os.path.join(os.path.dirname(__file__), "..", "data", file_name)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(file_name):
    path = os.path.join(os.path.dirname(__file__), "..", "data", file_name)
    with open(path, encoding="utf-8") as f:
        return json.load(f)

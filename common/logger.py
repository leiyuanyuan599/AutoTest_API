#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project   : 
@File      : logger.py
@Time      : 2025/10/13 15:23
@Author    : LeiYuanyuan
@Desc      :
"""
import logging
import sys


def get_logger(name="BaseRequest"):
    logger = logging.getLogger(name)
    if not logger.handlers:  # 防止重复挂 handler
        logger.setLevel(logging.INFO)
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s", "%H:%M:%S"))
        logger.addHandler(sh)
    return logger


logger = get_logger()

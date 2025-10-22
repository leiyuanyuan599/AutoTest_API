#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project   : 
@File      : config.py
@Time      : 2025/10/14 11:10
@Author    : LeiYuanyuan
@Desc      :
"""
import os
# 相关模块绝对路径
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_path = os.path.join(root_path, "data")
output_path = os.path.join(root_path, "outputs")
log_path = os.path.join(output_path, "logs")
allure_raw_path = os.path.join(output_path, "allure_raw")
allure_report_path = os.path.join(output_path, "allure_report")
testcases_path = os.path.join(root_path, "testcases")

# SMTP服务器配置
smtp_config = {
    'host': 'smtp.qq.com',  # SMTP服务商
    'port': 465,  # 端口
    'use_ssl': True,  # 是否开启安全认证
    'username': '2812995341@qq.com',  # 邮箱名称
    'password': 'ibjhjvflfzwzdgfe'  # 或邮箱授权码
}
# 发件人
sender = '2812995341@qq.com'
# 收件人
receivers = ['liuquan@paycools.com']

# 飞书群机器人Webhook地址
webhook_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/27ffaa1c-e24f-46fc-9111-1ff837ab9577'

# 公共请求头
com_headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6MTc0OTUyODAyNzkyMywidXNlcl9pZCI6MjE1LCJjYWNoZV9rZXkiOiJUT0tFTl9NR1JfMjE1In0.DLE69lIo5HEwu6rC-P0f-fdktpDzlv4UVi_k0_KVkos',
    'Host': 'mgr-dev.paycools.com:8199'}

# 错误的私钥
error_merchant_private_key = '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'

# 商户黑白名单相关ip
ip_dict = {
    'white_ip_legal': '47.107.124.35,192.168.40.149,192.168.40.13',
    'white_ip_illegal': '47.107.124.3,192.168.40.14,192.168.40.1',
    'black_ip_legal': '192.168.40.1',
    'black_ip_illegal': '192.168.40.13',
    'black_ip_legal_ph': '47.107.124.3',
    'black_ip_illegal_ph': '47.107.124.35'
}

# 用户mfa相关信息
user_mfa_dict = {
    "菲律宾": {"aesKey": "xo1WtQeA34DRMzHM", "aesIv": "xD086TwsO1JjWzBS"},
    "ezpay": {"aesKey": "hUBnOj6iPeNscgGa", "aesIv": "W3rjTdPZvLdaHalF"},
    "Paycools国际": {"aesKey": "hUBnOj6iPeNscgGa", "aesIv": "W3rjTdPZvLdaHalF"},
    "印尼": {"aesKey": "hUBnOj6iPeNscgGa", "aesIv": "W3rjTdPZvLdaHalF"},
    "马来": {"aesKey": "hUBnOj6iPeNscgGa", "aesIv": "W3rjTdPZvLdaHalF"},
    "Bluepay": {"aesKey": "hUBnOj6iPeNscgGa", "aesIv": "W3rjTdPZvLdaHalF"},
    "餐饮": {"aesKey": "SrHyHYXrijOGqvLJ", "aesIv": "Jhi3V2dbmJ8g3EGH"}
}

# 数据库连接相关信息
db_connect_info_dict = {
    "菲律宾1": {"host": "rm-3ns8772x1029i6l6r2o.mysql.rds.aliyuncs.com",
                "port": 3306,
                "user": "paycools_dev",
                "password": "823aDSsdD8S9!sDdf#D23DS3D"},
    "菲律宾2": {"host": "pc-3nspcev80r7g4c01h-public.rwlb.rds.aliyuncs.com",
                "port": 3306,
                "user": "paycools_dev",
                "password": "823aDSsdD8S9!sDdf#D23DS3D"},
    "ezpay": {"host": "database-test.cluster-cpkeh5sflgv6.ap-southeast-1.rds.amazonaws.com",
              "port": 3306,
              "user": "money_dev",
              "password": "RPPhSQg82U%WfaG"},
    "Paycools国际": {"host": "database-test.cluster-cpkeh5sflgv6.ap-southeast-1.rds.amazonaws.com",
                     "port": 3306,
                     "user": "money_dev",
                     "password": "RPPhSQg82U%WfaG"},
    "印尼": {"host": "ddd02.v6.rocks",
             "port": 13306,
             "user": "ez_dev",
             "password": "RPPhSQg82U%WfaG"},
    "马来": {"host": "ddd02.v6.rocks",
             "port": 13306,
             "user": "mapay_dev",
             "password": "RPPhSQg82U%WfaG"},
    "Bluepay": {"host": "gz-cynosdbmysql-grp-1jzs9bg1.sql.tencentcdb.com",
                "port": 22050,
                "user": "bluepay_dev",
                "password": "RPPhSQg82U%WfaG"},
    "餐饮": {"host": "ddd02.v6.rocks",
             "port": 13306,
             "user": "food_dev",
             "password": "RPPhSQg82U%WfaG"}
}

# redis连接相关信息
redis_connect_info_dict = {
    "菲律宾1": {"host": "10.88.88.5",
                "port": 6379,
                "password": "vNKoUqr388th4miYAp2i",
                "db": 1,
                "decode_responses": True},
    "菲律宾2": {"host": "10.88.88.5",
                "port": 6379,
                "password": "vNKoUqr388th4miYAp2i",
                "db": 2,
                "decode_responses": True},
    "ezpay": {"host": "192.168.41.51",
              "port": 8402,
              "password": "890234",
              "db": 0,
              "decode_responses": True},
    "Paycools国际": {"host": "192.168.41.51",
                     "port": 8402,
                     "password": "890234",
                     "db": 0,
                     "decode_responses": True},
    "印尼": {"host": "192.168.41.51",
             "port": 8402,
             "password": "890234",
             "db": 2,
             "decode_responses": True},
    "马来": {"host": "192.168.41.51",
             "port": 8402,
             "password": "890234",
             "db": 1,
             "decode_responses": True},
    "Bluepay": {"host": "192.168.41.51",
                "port": 8402,
                "password": "890234",
                "db": 6,
                "decode_responses": True},
    "餐饮": {"host": "192.168.41.51",
             "port": 8402,
             "password": "890234",
             "db": 8,
             "decode_responses": True}
}

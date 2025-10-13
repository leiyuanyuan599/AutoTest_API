#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project   : 
@File      : BaseRequest.py
@Time      : 2025/10/13 15:44
@Author    : LeiYuanyuan
@Desc      :
"""
import base64
import json
import requests

from common.crypto_utils import (
    aes_encrypt, aes_decrypt,
    sm4_encrypt, sm4_decrypt,
    des3_encrypt, des3_decrypt,
    rsa_sign
)
from common.logger import logger
from common.settings import base_url


class BaseRequest:
    _support_encrypt = {"aes", "sm4", "des3"}

    def __init__(self, encrypt_type=None, key=None, iv=None, sign_key=None, token=None, appname=None):
        self.s = requests.Session()
        self.s.headers.update({"Content-Type": "application/json"})
        self.encrypt_type = encrypt_type
        self.key, self.iv, self.sign_key = key, iv, sign_key
        self.token = token
        self.appname = appname

        # ===== 私有工具 =====

    def _encrypt_body(self, data: dict) -> str:
        """dict -> json-str -> encrypt -> base64"""
        plaintext = json.dumps(data, separators=(',', ':')).encode()
        if self.encrypt_type == "aes":
            return aes_encrypt(self.key, plaintext, self.iv)
        if self.encrypt_type == "sm4":
            return sm4_encrypt(self.key, plaintext)
        if self.encrypt_type == "des3":
            return des3_encrypt(self.key, plaintext, self.iv)
        raise ValueError(f"unsupported encrypt_type:{self.encrypt_type}")

    def _decrypt_resp(self, cipher_text: str) -> dict:
        b = base64.b64decode(cipher_text)
        if self.encrypt_type == "aes":
            return json.loads(aes_decrypt(self.key, cipher_text, self.iv))
        if self.encrypt_type == "sm4":
            return json.loads(sm4_decrypt(self.key, cipher_text))
        if self.encrypt_type == "des3":
            return json.loads(des3_decrypt(self.key, cipher_text, self.iv))

    def _apply_auth(self):
        """Bearer Token 支持外部刷新"""
        if self.token:
            self.s.headers.update({"Authorization": f"Bearer {self.token}"})

    def _apply_sign(self, body_str: str) -> str:
        """RSA SHA256 签名 -> base64"""
        return rsa_sign(self.sign_key, body_str.encode())

        # ===== 核心：send 方法 =====

    def send(self, method, url, payload: dict = None, **kwargs):
        self._apply_auth()
        url = base_url(self.appname) + url

        # ===== 1. 组装请求报文 =====
        if payload is None:
            data = None
        elif self.encrypt_type and self.key:
            cipher = self._encrypt_body(payload)
            data = json.dumps({"cipherText": cipher})
            if self.sign_key:
                data += f"&signature={self._apply_sign(data)}"
        else:
            data = json.dumps(payload, separators=(',', ':'))
            if self.sign_key:
                data += f"&signature={self._apply_sign(data)}"

        # ===== 2. 控制台打印（兼容加密模式） =====
        logger.info(f"▶️  {method.upper()}  {url}")
        if self.s.headers:
            logger.info(f"🔑  Headers: {json.dumps(dict(self.s.headers), ensure_ascii=False)}")
        if data:
            # 不打印真实密钥，只给提示
            print_payload = {"cipherText": "<encrypted>"} if self.encrypt_type else payload
            logger.info(f"📦  Body: {json.dumps(print_payload, ensure_ascii=False, indent=None)}")

        # ===== 3. 真正发请求 =====
        resp = self.s.request(method, url, data=data, **kwargs)

        # ===== 4. 打印返回 =====
        try:
            ret = resp.json()
            ret_print = {"<encrypted>": ret.get("cipherText")} if self.encrypt_type and ret.get("cipherText") else ret
        except Exception:
            ret_print = resp.text
        logger.info(f"⬅️  Response[{resp.status_code}]: {json.dumps(ret_print, ensure_ascii=False, indent=None)}")

        # ===== 5. 解密 & 返回 =====
        if self.encrypt_type and resp.text:
            try:
                cipher = resp.json().get("cipherText")
                return self._decrypt_resp(cipher)
            except Exception:
                return resp.json()
        return resp.json()

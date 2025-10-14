#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project   : 
@File      : crypto_utils.py
@Time      : 2025/10/13 15:31
@Author    : LeiYuanyuan
@Desc      : 金融常用对称/非对称加密工具集,return 统一 base64 字符串（便于 JSON 序列化）
"""

import base64
import random
import string
from Crypto.Cipher import PKCS1_v1_5, AES, DES3
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15


def generate_random_string(length: int = 16) -> str:
    """
    生成一个由大小写字母和数字组成的随机字符串，默认长度16
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# ----------- 1. RSA ---------------
def rsa_encrypt(public_key: str, plaintext: bytes) -> str:
    """public_key: PEM 格式秘钥字符串 (PKCS#8)"""
    key = RSA.import_key(public_key)
    cipher = PKCS1_v1_5.new(key)
    return base64.b64encode(cipher.encrypt(plaintext)).decode()


def rsa_decrypt(private_key: str, ciphertext: str) -> bytes:
    key = RSA.import_key(private_key)
    cipher = PKCS1_v1_5.new(key)
    return cipher.decrypt(base64.b64decode(ciphertext), None)


# ----------- RSA 签名/验签 -----------
def rsa_sign(private_key: str, message: bytes) -> str:
    """RSA SHA256 签名 -> base64"""
    key = RSA.import_key(private_key)
    h = SHA256.new(message)
    signature = pkcs1_15.new(key).sign(h)
    return base64.b64encode(signature).decode()


def rsa_verify(public_key: str, message: bytes, signature: str) -> bool:
    """验签 -> True/False"""
    key = RSA.import_key(public_key)
    h = SHA256.new(message)
    try:
        pkcs1_15.new(key).verify(h, base64.b64decode(signature))
        return True
    except (ValueError, TypeError):
        return False


# ----------- 2. AES (CBC, 256) ---------------
def aes_encrypt(key: str, plaintext: bytes, iv: str) -> str:
    key_bytes = key.encode()[:16]      # 16 B AES-128
    iv_bytes = iv.encode()[:16]
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    ct_bytes = cipher.encrypt(pad(plaintext, AES.block_size))
    return base64.b64encode(ct_bytes).decode()


def aes_decrypt(key: str, ciphertext: str, iv: str) -> bytes:
    key_bytes = key.encode()[:16]
    iv_bytes = iv.encode()[:16]
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    return unpad(cipher.decrypt(base64.b64decode(ciphertext)), AES.block_size)


# ----------- 3. SM4 (ECB) 国密 ---------------
def sm4_encrypt(key: bytes, plaintext: bytes) -> str:
    """key: 16 bytes"""
    sm4 = CryptSM4()
    sm4.set_key(key, SM4_ENCRYPT)
    ct_bytes = sm4.crypt_ecb(plaintext)
    return base64.b64encode(ct_bytes).decode()


def sm4_decrypt(key: bytes, ciphertext: str) -> bytes:
    sm4 = CryptSM4()
    sm4.set_key(key, SM4_DECRYPT)
    return sm4.crypt_ecb(base64.b64decode(ciphertext))


# ----------- 4. 3DES (CBC) ---------------
def des3_encrypt(key: bytes, plaintext: bytes, iv: bytes) -> str:
    """key: 24 bytes, iv: 8 bytes"""
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    ct_bytes = cipher.encrypt(pad(plaintext, DES3.block_size))
    return base64.b64encode(ct_bytes).decode()


def des3_decrypt(key: bytes, ciphertext: str, iv: bytes) -> bytes:
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    return unpad(cipher.decrypt(base64.b64decode(ciphertext)), DES3.block_size)


if __name__ == "__main__":
    text = b"hello finance"
    # RSA
    rsa_key = RSA.generate(2048)
    pub_pem = rsa_key.publickey().export_key()
    prv_pem = rsa_key.export_key()
    rsa_ct = rsa_encrypt(pub_pem.decode(), text)
    assert rsa_decrypt(prv_pem.decode(), rsa_ct) == text
    print("RSA OK")

    # AES
    aes_key, aes_iv = b"0" * 32, b"1" * 16
    aes_ct = aes_encrypt(aes_key, text, aes_iv)
    assert aes_decrypt(aes_key, aes_ct, aes_iv) == text
    print("AES OK")

    # SM4
    sm4_key = b"2" * 16
    sm4_ct = sm4_encrypt(sm4_key, text)
    assert sm4_decrypt(sm4_key, sm4_ct) == text
    print("SM4 OK")

    # 3DES
    des3_key, des3_iv = b"3" * 24, b"4" * 8
    des3_ct = des3_encrypt(des3_key, text, des3_iv)
    assert des3_decrypt(des3_key, des3_ct, des3_iv) == text
    print("3DES OK")

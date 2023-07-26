# -*- coding: utf-8 -*-
import json
import requests
import random
import sched
import hashlib
import urllib3
import time
import base64
from datetime import datetime
import importlib, sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import time
import binascii
serveSendKey = "SCT189646TxhAkXWXekyi6zZLrjJusbN9m"  # serve酱KEY http://sc.ftqq.com/?c=wechat&a=bind

def sendMsg(title, desp):
    url = "https://sctapi.ftqq.com/" + serveSendKey + ".send"
    body = {
        "title": title,
        "desp": desp
    }
    res = requests.post(url=url, data=body)
    print(res.text)

# sendMsg("测试标题","测试内容")

def decrypt(decrData):
    password = "23DbtQHR2UMbH6mJ"
    if isinstance(password, str):
        password = password.encode('utf8')

    cipher = AES.new(password, AES.MODE_ECB)
    plain_text = cipher.decrypt(binascii.a2b_hex(decrData))
    return plain_text.decode('utf8').rstrip('')

# def de():
# name = "436371ba0968da3fbd53382e9ea22d79"
data = "b4f69f6de545456a8f043249f0011a46"
data = decrypt(data)
# name[:3]
print(data)
# name = name[:3]
# sendMsg(name, "测试内容")

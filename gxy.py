# -*- coding: utf-8 -*-
import json
import requests
import random
import sched
import hashlib
import urllib3
from datetime import datetime
import importlib, sys
from Crypto.Cipher import AES
import time
import binascii

current_milli_time = lambda: int(round(time.time() * 1000))

# =================
# 问题集：
# python测试版本：3.6.6 如无法运行 请切换python版本
# pip pycrypto模块，报错参考：https://blog.csdn.net/qq_41917908/article/details/92612142
# 每天定时自动打卡 参考：https://www.lxlinux.net/525.html?ivk_sa=1024320u
# =================用户配置  可修改=======================

phone = ""  # 账号
password = ""  # 密码
country = ""  # 国家
province = ""  # 省
city = ""  # 城市
district = ""
address = "xx省 · xx市 · xx区 · xxxx"  # 地址
lat = ""  # 纬度   https://lbs.amap.com/tools/picker 根据地址找经纬度
lon = ""  # 经度   https://lbs.amap.com/tools/picker 根据地址找经纬度
# 打卡类型，START和END，START 上班，END 下班  执行时间会改变 这里默认12点前上班 不然下班 具体参考114行
types = "START"
description = ""
sec = 10  # 随机在0~sec秒执行打卡
isWeekCloak = True  # 周末是否打卡  True 可以  False 不可
serveSendKey = "SCT189646TxhAkXWXekyi6zZLrjJusbN9m"  # serve酱KEY http://sc.ftqq.com/?c=wechat&a=bind

# =================！！！！！以下内容不建议修改！！！！！！=======================
# =================！！！！！以下内容不建议修改！！！！！！=======================
# =================！！！！！以下内容不建议修改！！！！！！=======================
# =================！！！！！以下内容不建议修改！！！！！！=======================
# =================！！！！！以下内容不建议修改！！！！！！=======================

importlib.reload(sys)
# sys.setdefaultencoding("utf-8")
today = datetime.today().weekday()  # 获取今天星期几

urllib3.disable_warnings()


# requests.packages.urllib3.disable_warnings()


# =================工学云加密解密=======================
def encrypt(data):
    password = "23DbtQHR2UMbH6mJ"
    if isinstance(password, str):
        password = password.encode('utf8')

    bs = AES.block_size
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    cipher = AES.new(password, AES.MODE_ECB)
    data = cipher.encrypt(pad(data).encode('utf8'))
    encrypt_data = binascii.b2a_hex(data)  # 输出hex
    # encrypt_data = base64.b64encode(data)         # 取消注释，输出Base64格式
    return encrypt_data.decode('utf8')


def decrypt(decrData):
    password = "23DbtQHR2UMbH6mJ"
    if isinstance(password, str):
        password = password.encode('utf8')

    cipher = AES.new(password, AES.MODE_ECB)
    plain_text = cipher.decrypt(binascii.a2b_hex(decrData))
    return plain_text.decode('utf8').rstrip('')


# ===================基础变量不建议修改=============================
def getNowHour(oldTime):  # 时间换算
    if (oldTime + 8 > 24):
        return oldTime + 8 - 24
    else:
        return oldTime + 8


now_hour = getNowHour(time.gmtime()[3])  # 获取中国时间 小时
typeDec = ''  # 上班类型
# =================脚本配置(不可擅自更改)=======================
inc = random.randint(0, sec)
schedule = sched.scheduler(time.time, time.sleep)
ran = random.uniform(-0.003, 0.003)  # 随机300m坐标
latitude = str(ran + float(lat))
longitude = str(ran + float(lon))
Login_Url = 'https://api.moguding.net:9000/session/user/v3/login'
planUrl = "https://api.moguding.net:9000/practice/plan/v3/getPlanByStu"
saveUrl = "https://api.moguding.net:9000/attendence/clock/v2/save"
salt = "3478cbbc33f84bd00d75d7dfa69e0daa"
token = ""
headers = {
    "Host": "api.moguding.net:9000",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "User-Agent": "Mozilla/5.0 (Linux; Android 11.0; HTC M9e Build/EZG0TF) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.1566.54 Mobile Safari/537.36",
    "sign": "",
    "Authorization": "",
    "roleKey": "student",
    "Content-Type": "application/json; charset=UTF-8",
    "Accept-Encoding": ""
}
if (now_hour < 12):
    types = "START"
    typeDec = '上班'
else:
    types = "END"
    typeDec = '下班'
body = {
    "country": country,
    "address": address,
    "province": province,
    "city": city,
    "latitude": latitude,
    "description": description,
    "type": types,
    "device": "Android",
    "longitude": longitude
}


# ===============================serve酱推送=====================
def sendMsg(title, desp):
    url = "https://sctapi.ftqq.com/" + serveSendKey + ".send"
    body = {
        "title": title,
        "desp": desp
    }
    print(title)
    print(desp)
    res = requests.post(url=url, data=body)
    print(res.text)


# =================生成签名===================
def GenerateSign(x):
    a = x.encode('utf-8')
    a = hashlib.md5(a).hexdigest()
    # print(a)
    return a


# ================登录====================


def login():
    global token, userId, name
    # print(encrypt(phone).upper())
    # print(encrypt(password).upper())
    # print(encrypt(str(current_milli_time())).upper())
    data = {
        "password": str(encrypt(password).upper()),
        "t": str(encrypt(str(current_milli_time())).upper()),
        "loginType": "android",
        "uuid": "",
        "phone": str(encrypt(phone).upper())
    }
    req = requests.post(Login_Url, data=json.dumps(data), headers=headers)
    text = req.json()
    # print(req.text)
    new_token = text["data"]["token"]
    name = text["data"]["nikeName"]
    name = decrypt(name)
    name = name[:3]
    token = json.loads(req.text)['data']['token']
    userId = json.loads(req.text)['data']['userId']


# ===================获取planID=======================
def getPlanId():
    login()

    global planId
    data = {"state": ""}
    headers["Authorization"] = token
    # sign= userId+"student"+salt
    headers["sign"] = GenerateSign(userId + "student" + salt)
    req = requests.post(planUrl, data=json.dumps(data), headers=headers)
    req.headers.keys()
    planId = json.loads(req.text)['data'][0]['planId']


# =======================开始打卡=======================
def main():
    getPlanId()

    # sign= device + type + planID + userId + Address + salt
    body["planId"] = planId
    headers["sign"] = GenerateSign(body["device"] + body["type"] + planId + userId + body["address"] + salt)
    req = requests.post(saveUrl, data=json.dumps(body), headers=headers)
    req_json = json.loads(req.text)

    if (req_json["code"] == 200):
        # print(name + "打卡成功")
        sendMsg("Hi," + name + typeDec + "打卡成功",
                "打卡状态：" + req_json["msg"] + "\n\n打卡地点：" + address + "\n\n打卡时间：" + req_json["data"]["createTime"])
    else:
        print(name + "打卡失败")
        sendMsg("蘑菇丁打卡失败", "打卡失败" + "失败原因：" + req_json["msg"])


if (isWeekCloak):
    schedule.enter(inc, 0, main, ())
    schedule.run()
else:
    if (today < 5):
        schedule.enter(inc, 0, main, ())
        schedule.run()
    else:
        print("周末不签到")

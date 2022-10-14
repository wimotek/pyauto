# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/10/14
# @Author  : 智多科技wimotek.com
# @File    : could_189_cn.py
# @Software: IDLE

'''
cron:  30 0 * * * CLOUD_189_CN.py
new Env('天翼云签到脚本');
'''
import os
import time
import logging
import base64
import re
import time
import requests
import rsa

# 日志模块
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logFormat = logging.Formatter("%(message)s")

# 日志输出流
stream = logging.StreamHandler()
stream.setFormatter(logFormat)
logger.addHandler(stream)
#本地使用
#os.environ["CLOUD_189_CN"]=''
    
# 配信文件
try:
    from sendNotify import send
except Exception as error:
    logger.info('推送文件有误')
    logger.info(f'失败原因:{error}')
    sys.exit(0)

# 配信内容格式
allMess = ''
def notify(content=None):
    global allMess
    allMess = allMess + content + '\n'
    logger.info(content)

# 导入账户
CLOUD_189_CN=''
if "CLOUD_189_CN" in os.environ and os.environ["CLOUD_189_CN"]:
    CLOUD_189_CN = os.environ["CLOUD_189_CN"]
if CLOUD_189_CN:
    userpasswordArr= CLOUD_189_CN.split("@")
else:
    logger.info(f'失败原因:请配置环境变量CLOUD_189_CN.帐户与密码用&连接, 多帐号用@隔开')
    sys.exit(0)
    
# 日志录入时间
notify(f"任务:天翼云签到脚本\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")

class CheckIn(object):
    client = requests.Session()
    login_url = "https://cloud.189.cn/api/portal/loginUrl.action?" \
                "redirectURL=https://cloud.189.cn/web/redirect.html?returnURL=/main.action"
    submit_login_url = "https://open.e.189.cn/api/logbox/oauth2/loginSubmit.do"
    sign_url = ("https://api.cloud.189.cn/mkt/userSign.action?rand=%s"
                "&clientType=TELEANDROID&version=8.6.3&model=SM-G930K")

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_in(self):
        self.login()
        rand = str(round(time.time() * 1000))
        url = "https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN&activityId=ACT_SIGNIN"
        url2 = "https://m.cloud.189.cn/v2/drawPrizeMarketDetails.action?taskId=TASK_SIGNIN_PHOTOS&activityId=ACT_SIGNIN"
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv)"
                          " AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74"
                          ".0.3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clie"
                          "ntId/355325117317828 clientModel/SM-G930K imsi/46007111431782"
                          "4 clientChannelId/qq proVersion/1.0.6",
            "Referer": "https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1",
            "Host": "m.cloud.189.cn",
            "Accept-Encoding": "gzip, deflate",
        }
        response = self.client.get(self.sign_url % rand, headers=headers)
        net_disk_bonus = response.json()["netdiskBonus"]
        if response.json()["isSign"] == "false":
            print(f"未签到，签到获得{net_disk_bonus}M空间")
        else:
            print(f"已经签到过了，签到获得{net_disk_bonus}M空间")
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G930K Build/NRD90M; wv) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0"
                          ".3729.136 Mobile Safari/537.36 Ecloud/8.6.3 Android/22 clientI"
                          "d/355325117317828 clientModel/SM-G930K imsi/460071114317824 cl"
                          "ientChannelId/qq proVersion/1.0.6",
            "Referer": "https://m.cloud.189.cn/zhuanti/2016/sign/index.jsp?albumBackupOpened=1",
            "Host": "m.cloud.189.cn",
            "Accept-Encoding": "gzip, deflate",
        }
        response = self.client.get(url, headers=headers)
        if "errorCode" in response.text:
            print(response.text)
        else:
            prize_name = (response.json() or {}).get("prizeName")
            print(f"抽奖获得{prize_name}")
        response = self.client.get(url2, headers=headers)
        if "errorCode" in response.text:
            print(response.text)
        else:
            prize_name = (response.json() or {}).get("prizeName")
            print(f"抽奖获得{prize_name}")

    @staticmethod
    def rsa_encode(rsa_key, string):
        rsa_key = f"-----BEGIN PUBLIC KEY-----\n{rsa_key}\n-----END PUBLIC KEY-----"
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(rsa_key.encode())
        result = b64_to_hex((base64.b64encode(rsa.encrypt(f"{string}".encode(), pubkey))).decode())
        return result

    def login(self):
        r = self.client.get(self.login_url)
        captcha_token = re.findall(r"captchaToken' value='(.+?)'", r.text)[0]
        lt = re.findall(r'lt = "(.+?)"', r.text)[0]
        return_url = re.findall(r"returnUrl = '(.+?)'", r.text)[0]
        param_id = re.findall(r'paramId = "(.+?)"', r.text)[0]
        j_rsa_key = re.findall(r'j_rsaKey" value="(\S+)"', r.text, re.M)[0]
        self.client.headers.update({"lt": lt})
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/76.0",
            "Referer": "https://open.e.189.cn/",
        }
        data = {
            "appKey": "cloud",
            "accountType": "01",
            "userName": f"{{RSA}}{self.rsa_encode(j_rsa_key, self.username)}",
            "password": f"{{RSA}}{self.rsa_encode(j_rsa_key, self.password)}",
            "validateCode": "",
            "captchaToken": captcha_token,
            "returnUrl": return_url,
            "mailSuffix": "@189.cn",
            "paramId": param_id,
        }
        r = self.client.post(self.submit_login_url, data=data, headers=headers, timeout=5)
        print(r.json()["msg"])
        if '图形验证码错误' in r.json()["msg"]:
            raise Exception("账户需输入验证码，请手动在app登录一次或修改密码后重试脚本")
        redirect_url = r.json()["toUrl"]
        self.client.get(redirect_url)


def _chr(a):
    return "0123456789abcdefghijklmnopqrstuvwxyz"[a]


b64map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def b64_to_hex(a):
    d = ""
    e = 0
    c = 0
    for i in range(len(a)):
        if list(a)[i] != "=":
            v = b64map.index(list(a)[i])
            if 0 == e:
                e = 1
                d += _chr(v >> 2)
                c = 3 & v
            elif 1 == e:
                e = 2
                d += _chr(c << 2 | v >> 4)
                c = 15 & v
            elif 2 == e:
                e = 3
                d += _chr(c)
                d += _chr(v >> 2)
                c = 3 & v
            else:
                e = 0
                d += _chr(c << 2 | v >> 4)
                d += _chr(15 & v)
    if e == 1:
        d += _chr(c << 2)
    return d


if __name__ == "__main__":
    for item in userpasswordArr:
        userpassword=item.split('&')
        user=userpassword[0]
        password=userpassword[1]
        notify(f'准备签到帐号:{user}')
        try:
           helper = CheckIn(user, password)
           helper.check_in()
        except Exception as err :
            notify(f'发生错误:{err}')

    send('天翼云签到脚本',allMess)
    

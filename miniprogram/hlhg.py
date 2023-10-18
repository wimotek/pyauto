# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26
# @Author  : 智多科技www.wimotek.com 交流群:34989949
# @File    : digit_cn.py
# @Software: IDLE

'''
cron:  16 7 * * * hlgw.py
new Env('欢乐港湾签到');
'''
import os
import re
import sys
import json
import time
import random
import requests
import logging


# 日志模块
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logFormat = logging.Formatter("%(message)s")

# 日志输出流
stream = logging.StreamHandler()
stream.setFormatter(logFormat)
logger.addHandler(stream)

os.environ["hlgw_COOKIE"]='WeixinMiniToken:542:a36495f6c948795d1868c463b17ee1d59102eb96'
    
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
hlgw_COOKIE=''
if "hlgw_COOKIE" in os.environ and os.environ["hlgw_COOKIE"]:
    hlgw_COOKIE = os.environ["hlgw_COOKIE"]
if hlgw_COOKIE:
    ckArr= hlgw_COOKIE.split("@")
else:
    logger.info(f'失败原因:请配置环境变量hlgw_COOKIE')
    sys.exit(0)
    
# 日志录入时间
notify(f"任务:欢乐港湾签到\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")



def start():
  
  #Headers信息 
  headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; ANY-AN00 Build/HONORANY-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5235 MMWEBSDK/20230701 MMWEBID/2833 MicroMessenger/8.0.40.2420(0x28002855) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
        'Referer': 'https://servicewechat.com/wx7c9e21aa951ca0b8/77/page-frame.html',
        'token': ck,
        'mkey': 'ef2686aedc6808e094c274622367fe19',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'bid': 'jfdi',
        'version': '4.08.19',
        'ts': str(int(time.time())),
        'Host':'wox2019.woxshare.com',
        'Connection':'keep-alive'
  }

   
  try: 
    # 发送请求
    
    requests.adapters.DEFAULT_RETRIES = 5    #增加重连次数
    s = requests.session()
    s.keep_alive = False    #关闭多余连接
    #s.proxies = {"https": "101.133.231.6:80", "http": "106.14.255.124:80", }
    s.headers.update(headers)
    #登录
    #https://wox2019.woxshare.com/publicApi/weiXinAuthorizationUserSession
    #__json ={"appId":"wx7c9e21aa951ca0b8","js_code":"0d3I3BGa1RENdG0udpJa13OeXa3I3BGa","token": ck,"version":"4.08.19","bid":"jfdi","mkeyUrl":"/publicApi/weiXinAuthorizationUserSession","mkey":"502ae7cc55f6fd13bfe2397c4f5cbb938af37ea2"}
    #rsp_dict=s.post(url,json=__json).json()
    #print(rsp_dict)
    
    #签到
    __json ={
       "token": ck,
       "version":"4.08.19",
       "bid":"jfdi",
       "mkeyUrl":"/clientApi/signInRecordAdd",
       "mkey":"bfc26322fcf995a4e6ff0afc28389f7517e44920"
       }

    rsp_dict=s.post(sign_url,json=__json).json()
    
    print(rsp_dict)

    #推送消息
    if rsp_dict.get("errCode") == 0:
        notify(f'签到成功.已经签到{rsp_dict["detail"]["signDays"]}/3天.')
    else:
        notify(f'签到失败:{rsp_dict.get("errMsg")}')

    rsp_dict=s.post("https://wox2019.woxshare.com/clientApi/userCenterDetail",json=__json).json()
    notify(f'目前积分{rsp_dict["detail"]["userInfoDetail"]["integral"]}.')

  except Exception as error: 
    logger.info(f'失败原因:{error}')
    sys.exit(0)


if __name__ == '__main__':
    millisecond_time = round(time.time() * 1000)
    url='https://wox2019.woxshare.com/publicApi/weiXinAuthorizationUserSession'
    sign_url="https://wox2019.woxshare.com/clientApi/signInRecordAdd"
    
    for ck in ckArr:
       start()
    send('欢乐港湾签到',allMess)

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26
# @Author  : 智多科技www.wimotek.com 交流群:34989949
# @File    : digit_cn.py
# @Software: IDLE

'''
cron:  16 0 * * * V_QQ_COM.py
new Env('腾讯视频签到');
'''
import os
import re
import sys
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

#本地用
#os.environ["V_QQ_CN_COOKIE"]='tvfe_boss_uuid=1ec8e1bd5f73a024; pgv_pvid=732836017; video_platform=2; video_guid=516e048c83a12e2eb4440f34036dd2e2; ptui_loginuin=25100295; RK=ae9YgWKhVC; ptcz=7aca5dbfdca341a8068baf21cfbbaa2900a20d85b4119581f564aaec852f517e; main_login=qq; vqq_access_token=A246CCFAB5E3B32891C77D600A11FB3B; vqq_appid=101483052; vqq_openid=73B08A20A40D5F45E39A2408D7DEEABB; vqq_vuserid=228012322; vqq_refresh_token=70A2184EC95A2347869482915AA3464D; pac_uid=0_aa8608140a2de; o_cookie=25100295; vqq_vusession=tNxxRYGnGurQWC8L_abwLw.N; vqq_next_refresh_time=6600; vqq_login_time_init=1652601691; pgv_info=ssid=s2071449216; login_time_last=2022-5-15 16:1:34'
    
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
V_QQ_CN_COOKIE=''
if "MYDIGIT_COOKIE" in os.environ and os.environ["V_QQ_CN_COOKIE"]:
    MYDIGIT_COOKIE = os.environ["V_QQ_CN_COOKIE"]
if MYDIGIT_COOKIE:
    ckArr= MYDIGIT_COOKIE.split("@")
else:
    logger.info(f'失败原因:请配置环境变量V_QQ_CN_COOKIE')
    sys.exit(0)
    
# 日志录入时间
notify(f"任务:数码之家签到\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")



def start():
  
  #Headers信息
  headers = {
        'Referer': 'https://v.qq.com',
  }
  ck= requests.utils.dict_from_cookiejar(ck)

  try: 
    # 发送请求
    
    requests.adapters.DEFAULT_RETRIES = 5    #增加重连次数
    s = requests.session()
    s.keep_alive = False    #关闭多余连接
    #s.proxies = {"https": "101.133.231.6:80", "http": "106.14.255.124:80", }
    s.headers.update(headers)
    s.cookies.update(ck)

    #登录
    res=s.get(url)
    cookie = requests.utils.dict_from_cookiejar(res.cookies)
    print(ck)
    print("=====>",cookie)
    ck['vqq_vusession']=cookie['vqq_vusession']
    s.cookies.update(ck)
    #签到
    res=s.get(sign_url)
    #print("==>",res.text)

    #推送消息
    if 'Account Verify Error' in sign:
        notify(f"签到失败")
    else:
        notify(f"签到成功")

  except Exception as error: 
    logger.info(f'失败原因:{error}')
    sys.exit(0)


if __name__ == '__main__':
    url='https://access.video.qq.com/user/auth_refresh?type=qq&g_vstk=640926988&g_actk=768564498&raw=1&vappid=11059694&vsecret=fdf61a6be0aad57132bc5cdf78ac30145b6cd2c1470b0cfe'
    sign_url='https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2'
    
    for ck in ckArr:
       start()
    send('腾讯视频签到',allMess)

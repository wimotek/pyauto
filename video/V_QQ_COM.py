# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26
# @Author  : 智多科技www.wimotek.com 交流群:34989949
# @File    : V_QQ_COM.py
# @Software: IDLE

'''
cron:  16 0 * * * V_QQ_COM.py
new Env('腾讯视频签到');
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

#本地配置
#os.environ["V_QQ_COM_COOKIE"]=''
    
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
V_QQ_COM_COOKIE=''
if "V_QQ_COM_COOKIE" in os.environ and os.environ["V_QQ_COM_COOKIE"]:
   V_QQ_COM_COOKIE = os.environ["V_QQ_COM_COOKIE"]
if V_QQ_COM_COOKIE:
    ckArr= V_QQ_COM_COOKIE.split("@")
else:
    logger.info(f'失败原因:请配置环境变量V_QQ_COM_COOKIE')
    sys.exit(0)
    
# 日志录入时间
notify(f"任务:腾讯视频签到\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")



def start():
  
  #Headers信息
  headers = {
         "User-Agent": "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; Mi Note 3 Build/OPM1.171019.019) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 "
                       "Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.0.2",
        'Referer': 'https://v.qq.com',
        'Cookie':ck
  }
   
  try: 
    # 发送请求
    
    requests.adapters.DEFAULT_RETRIES = 5    #增加重连次数
    s = requests.session()
    s.keep_alive = False    #关闭多余连接
    #s.proxies = {"https": "101.133.231.6:80", "http": "106.14.255.124:80", }
    s.headers.update(headers)
    #登录
    res=s.get(url)
    #签到
    res=s.get(sign_url).text
    #logger.info(res)
    #推送消息
    # QZOutputJson=({ "ret": 0,"checkin_score": 0,"msg":"OK"});
    # QZOutputJson=({"msg":"Account Verify Error","ret":-10006});
    start_index = res.index("(")
    end_index = res.index(")")
    rsp_dict = json.loads(res[start_index + 1:end_index])

    if rsp_dict.get("ret") == -10006:
        notify(f"签到失败:COOKIE失效")
    elif rsp_dict.get("ret") == 0:
        notify(f"签到成功")
    else:
        notify(f"签到失败:未知错误")

  except Exception as error: 
    logger.info(f'失败原因:{error}')
    sys.exit(0)


if __name__ == '__main__':
    millisecond_time = round(time.time() * 1000)
    url='https://access.video.qq.com/user/auth_refresh?type=qq&g_vstk=640926988&g_actk=768564498&raw=1&vappid=11059694&vsecret=fdf61a6be0aad57132bc5cdf78ac30145b6cd2c1470b0cfe'
    sign_url='https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2'f"&_={str(millisecond_time)}"
    
    for ck in ckArr:
       start()
    send('腾讯视频签到',allMess)

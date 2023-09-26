# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26
# @Author  : 智多科技www.wimotek.com 交流群:34989949 转发请勿更改
# @File    : 22vd_com.py
# @Software: IDLE

'''
cron:  16 5,12 * * * 22vd_com.py
new Env('云模板签到');
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

#本地配置
#os.environ["22VD_COOKIE"]=''
    
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
22VD_COOKIE=''
if "22VD_COOKIE" in os.environ and os.environ["22VD_COOKIE"]:
    22VD_COOKIE = os.environ["22VD_COOKIE"]
if 22VD_COOKIE:
    ckArr= 22VD_COOKIE.split("@")
else:
    logger.info(f'失败原因:请配置环境变量22VD_COOKIE')
    sys.exit(0)
#本地测试:
22VD_COOKIE='Hm_lvt_8041e164e331efcd17a75126a3d7bc12=1695696191; myad=1; wordpress_logged_in_f60133e7528c48385cd3315bab925252=19219.666.25040864079b5967853781ff1b12c4c9%7C1696906240%7CuHtmyOPyeQ9hdmPU061sHT1T3dCrvOwgxbEAxuLJfYT%7C04bf8adec309a8dfa9997f33f11310a78805f93abf610be7c0df39d7f1be0dd1; wp_xh_session_f60133e7528c48385cd3315bab925252=d426e043a2b6eb81dcb23961c563016d%7C%7C1695869439%7C%7C1695865839%7C%7Cc2c6a88553e9950f36cb6f556b9d7f3f; pll_language=zh; PHPSESSID=us60e1c4kdcspsvnsgkb1icin2; Hm_lpvt_8041e164e331efcd17a75126a3d7bc12=1695698799; pupmove=true'
# 日志录入时间
notify(f"任务:云模板签到\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")



def start():
  
  #Headers信息
  headers = {
    'Connection': 'keep-alive',
    'User-Agnet': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47',
    'Cookie': ck,
    'Referer':'https://www.22VD.cn/sign',
    'action': "sign_ajax",
    'ajax_date': 'sign',
  }


  try: 
    # 发送请求
    
    requests.adapters.DEFAULT_RETRIES = 5    #增加重连次数
    s = requests.session()
    s.keep_alive = False    #关闭多余连接
    #s.proxies = {"https": "101.133.231.6:80", "http": "106.14.255.124:80", }
    s.headers.update(headers)
    #print(headers)

    res=s.get(url,allow_redirects=False).text
    #print("==>",res)

   
    #签到 
    payload: {
          action: "sign_ajax",
          ajax_date: 'sign'
          }
    
    res=s.post(sign_url,data=headers)
    #print("==>",res.text)
    print(res)

    #推送消息
    
    #<div><span class="title">连续签到：</span><span><b>(\d+)</b> 天</span></div>
    daynum=re.findall(r'连续签到：</span><span><b>(\d+)</b> 天</span></div>',res.text)
    if daynum:
        notify(f"连续签到{daynum[0]}天")
    else:
        notify(f"签到失败")

  except Exception as error: 
    logger.info(f'失败原因:{error}')
    sys.exit(0)


if __name__ == '__main__':
    url='https://www.22vd.com/sign'
    sign_url='https://www.22vd.com/wp-admin/admin-ajax.php'
    
    for ck in ckArr:
       start()
    send('云模板签到',allMess)


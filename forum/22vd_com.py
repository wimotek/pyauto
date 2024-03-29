# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26
# @Author  : 智多科技www.wimotek.com 交流群:34989949 转发请勿更改
# @File    : 22vd_com.py
# @Software: IDLE

'''
cron:  16 0 * * * raw_main_22vd_com.py
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
#os.environ["VD_COOKIE"]=''
    
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


#本地测试:
VD_COOKIE='pll_language=zh; wp_xh_session_f60133e7528c48385cd3315bab925252=683a3b1f29d2f08a6dfca9d1448f2555%7C%7C1696032634%7C%7C1696029034%7C%7Cb1480bb248ff2871598e53f7e7336635; Hm_lvt_8041e164e331efcd17a75126a3d7bc12=1695859835; myad=1; pupmove=true; wordpress_logged_in_f60133e7528c48385cd3315bab925252=19219.056.1335a0a192ddbcc1ea1c00b9dd7de3b7%7C1697069690%7ClMPmKIBmZHXT1hcIED5CUh5Wc1cuCKZdVI3Y7dYG2Fq%7Cb07e3a28edb464272841dbc3ca052557dbdc59f01237778c432232d74568aa3a; Hm_lpvt_8041e164e331efcd17a75126a3d7bc12=1695860162'

# 导入账户
#VD_COOKIE=''

if "VD_COOKIE" in os.environ and os.environ["VD_COOKIE"]:
    VD_COOKIE = os.environ["VD_COOKIE"]
if VD_COOKIE:
    ckArr= VD_COOKIE.split("@")
else:
    logger.info(f'失败原因:请配置环境变量VD_COOKIE')
    sys.exit(0)

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

    #res=s.get(url,allow_redirects=False).text
    #print("==>",res)

   
    #签到 
    payload: {
          action: "sign_ajax",
          ajax_date: 'sign'
          }
    
    res=s.post(sign_url,data=headers)
    if res.text=='2' :
      notify(f"您今天已经签到过了")
             
    #推送消息
    res=s.get(url,allow_redirects=False).text
    #print("==>",res)
    
    #<div><span class="title">连续签到：</span><span><b>(\d+)</b> 天</span></div>
    daynum=re.findall(r'连续签到：</span><span><b>(\d+)</b> 天</span></div>',res)
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

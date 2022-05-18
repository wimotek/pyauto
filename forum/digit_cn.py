# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26
# @Author  : 智多科技www.wimotek.com 交流群:34989949
# @File    : digit_cn.py
# @Software: IDLE

'''
cron:  16 5,12 * * * digit_cn.py
new Env('数码之家签到');
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

os.environ["MYDIGIT_COOKIE"]='VhUn_2132_saltkey=RObQXJjc; VhUn_2132_lastvisit=1652601034; VhUn_2132_auth=54ffEPYBZTWFDa1MMfimq3ujxqqneDLOw%2BmTtKtaqvKl%2BRXuXdXXSbcLUymXnJ7j8NNUH2kNrnOaOGTBRG77ckxMklGG; VhUn_2132_sid=0; VhUn_2132_connect_is_bind=1; VhUn_2132_nofavfid=1; VhUn_2132_ulastactivity=1652768740%7C0; VhUn_2132_lastcheckfeed=1867361%7C1652768742; VhUn_2132_sendmail=1; Hm_lvt_ab859ea8b00af2b447b0a7cdc5e2e13d=1652513384,1652603690,1652682985,1652768805; Hm_lpvt_ab859ea8b00af2b447b0a7cdc5e2e13d=1652768805; VhUn_2132_lastact=1652768745%09home.php%09spacecp'
    
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
MYDIGIT_COOKIE=''
if "MYDIGIT_COOKIE" in os.environ and os.environ["MYDIGIT_COOKIE"]:
    MYDIGIT_COOKIE = os.environ["MYDIGIT_COOKIE"]
if MYDIGIT_COOKIE:
    ckArr= MYDIGIT_COOKIE.split("@")
else:
    logger.info(f'失败原因:请配置环境变量MYDIGIT_COOKIE')
    sys.exit(0)
    
# 日志录入时间
notify(f"任务:数码之家签到\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")



def start():
  
  #Headers信息
  headers = {
    'Connection': 'keep-alive',
    'User-Agnet': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47',
    'Cookie': ck,
    'Referer':'https://www.mydigit.cn/forum.php',
  }


  try: 
    # 发送请求
    
    requests.adapters.DEFAULT_RETRIES = 5    #增加重连次数
    s = requests.session()
    s.keep_alive = False    #关闭多余连接
    #s.proxies = {"https": "101.133.231.6:80", "http": "106.14.255.124:80", }
    s.headers.update(headers)
    #print(headers)

    res=s.get(url).text
    #print("==>",res)

    #获取formhash
    formhash = re.findall(r'<input type=\"hidden\" name=\"formhash\" value=\"(.*?)\" />', res)

    
    #签到
    res=s.get(sign_url.replace("[@]",formhash[0]))
    #print("==>",res.text)

    #推送消息
    
    res=s.get(url)
    #print(res.text)
    
    daynum=re.findall(r'id="lxdays" value="(\d+)">',res.text)
    if daynum:
        notify(f"连续签到{daynum[0]}天")
    else:
        notify(f"签到失败")

    #随机访问一个用户
    res=s.get('https://www.mydigit.cn/plugin.php?id=k_misign:sign&operation=list').text
    list=re.findall(r'<a href="space\-uid\-(\d+)\.html"',res)
    id=random.randint(3,17)
    if id!=3 and id !=17:
      id-=1
    res=s.get("https://www.mydigit.cn/home.php?mod=space&uid=[@]&do=profile&from=space".replace('[@]',list[id]))
    if 200==res.status_code:
      notify(f"访问个人主页成功:{res.url}")
    else:
      notify(f"访问个人主页失败:{res}")

  except Exception as error: 
    logger.info(f'失败原因:{error}')
    sys.exit(0)


if __name__ == '__main__':
    url='https://www.mydigit.cn/k_misign-sign.html'
    sign_url='https://www.mydigit.cn/plugin.php?id=k_misign:sign&operation=qiandao&formhash=[@]&format=empty'
    
    for ck in ckArr:
       start()
    send('数码之家签到',allMess)

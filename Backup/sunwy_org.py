# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/26
# @Author  : 智多科技wimotek.com 欢迎转载,请勿更改来源信息.
# @File    : sunwy_org.py
# @Software: IDLE

'''
cron:  0 0 * * * sunwy_org.py
new Env('阳光驿站签到');
'''
import os
import sys
import time
import urllib.request,re
from urllib.parse import urlencode
from http import cookiejar
import logging


# 日志模块
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logFormat = logging.Formatter("%(message)s")

# 日志输出流
stream = logging.StreamHandler()
stream.setFormatter(logFormat)
logger.addHandler(stream)
#本地使用,用户名与密码用&隔开. 多用户之间用@隔开.
#os.environ["SUNWY_ORG"]='user&password'
    
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
SUNWY_ORG=''
if "SUNWY_ORG" in os.environ and os.environ["SUNWY_ORG"]:
    SUNWY_ORG = os.environ["SUNWY_ORG"]
if SUNWY_ORG:
    userpasswordArr= SUNWY_ORG.split("@")
else:
    logger.info(f'失败原因:请配置环境变量SUNWY_ORG.帐户与密码用&连接, 多帐号用@隔开')
    sys.exit(0)
    
# 日志录入时间
notify(f"任务:阳光驿站签到\n时间:{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())}")



def start():
 #Headers信息
  head = {
    'User-Agnet': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
    'Connection': 'keep-alive'
  }


  try: 
    #获得一个cookieJar实例 
    cj = cookiejar.CookieJar() 
    #cookieJar作为参数，获得一个opener的实例 
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)) 
    #伪装成一个正常的浏览器，避免有些web服务器拒绝访问。 
    opener.addheaders = [head]

    #生成Post数据，含有登陆用户名密码。 


    #登陆Form_Data信息
    Login_Data = {
      'username': user,
      'password': password
    }

    data = urlencode(Login_Data).encode('gbk')
    
    #以post的方法访问登陆页面，访问之后cookieJar会自定保存cookie
    content=opener.open(login_page,data=data).read().decode('gbk','ingore')
    notify("登录完成")


    #以带cookie的方式访问页面 

    
    c=opener.open(sign_url) .read().decode('gbk','ingore')
    formhash= re.findall(r'<input type=\"hidden\" name=\"formhash\" value=\"(.*?)\" />', c)

    if not formhash:
      raise Exception('签到 Fail!')
    formhash = formhash[0]
    post_data={
      'formhash': formhash,
      'qdxq': 'kx',
      'qdmode': '3',
      'todaysay': ''

    }
    data=urlencode(post_data).encode('gbk')

    content=opener.open(sign_submit,data=data) .read().decode('gbk',errors = 'ignore')
    notify("签到完成")

  except Exception as e: 
    print (str(e) )
    
if __name__ == '__main__':
    #登陆页面，可以通过抓包工具分析获得，如fiddler，wireshark 
    login_page = "https://bbs.sunwy.org/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes"
    sign_url='https://bbs.sunwy.org/plugin.php?id=dsu_paulsign:sign'
    sign_submit='https://bbs.sunwy.org/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=0&sign_as=1'
    
    for item in userpasswordArr:
        userpassword=item.split('&')
        user=userpassword[0]
        password=userpassword[1]
        start()
    send('阳光驿站签到',allMess)

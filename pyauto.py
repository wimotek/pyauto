import urllib.request,re,os
from urllib.parse import urlencode
from http import cookiejar

serverJ = os.getenv('PUSH_KEY');

def sendNotify (text,desp):
  api = "https://sc.ftqq.com/${serverJ}.send"
  data = {
    "text":text,
    "desp":desp
  }
  req = urllib.request.urlopen(api,data = data).read().decode('utf-8')
  return req

subject='测试'
message='from github'
result=sendNotify(subject,message)
print (result)

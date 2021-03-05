import urllib.request,re
from urllib.parse import urlencode
from http import cookiejar

serverJ = PUSH_KEY;


subject='测试'
message='from github'
result=sendNotify(subject,message)
print (result)

def sendNotify (text,desp):
  api = "https://sc.ftqq.com/${serverJ}.send"
  data = {
    "text":text,
    "desp":desp
  }
  req = urllib.request.urlopen(api,data = data).read().decode('utf-8')
  return req

import urllib.request,re,os
from urllib.parse import urlencode
from http import cookiejar

serverJ = os.environ.get('PUSH_KEY')
print(serverJ)

def sendNotify (text,desp):
  api = "https://sc.ftqq.com/${serverJ}.send"
  data = {
    "text":text,
    "desp":desp
  }
  data=urlencode(data).encode('utf-8',errors = 'ignore')
  req = urllib.request.urlopen(api,data = data).read().decode('utf-8')
  return req

subject='测试'
message='from github'
result=sendNotify(subject,message)
print (result)

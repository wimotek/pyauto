import urllib.request,re,os
from urllib.parse import urlencode
from http import cookiejar

serverJ = os.environ['PUSH_KEY']

def sendNotify (text,desp):
  api = 'https://sc.ftqq.com/{}.send'.format(serverJ)
  data = {
    "text":text,
    "desp":desp
  }
  data=urlencode(data).encode('utf-8',errors = 'ignore')
  req = urllib.request.urlopen(api,data = data).read().decode('utf-8')
  return req

subject='测试1'
message='from github'
result=sendNotify(subject,message)
print (result)

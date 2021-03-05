import urllib.request,re,requests
from urllib.parse import urlencode
from http import cookiejar

serverJ = process.env.PUSH_KEY;


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
 req = requests.post(api,data = data)
return req

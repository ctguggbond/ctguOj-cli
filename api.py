import requests
import pytesseract 
from PIL import Image
from io import BytesIO
import termcolor
from http import cookiejar
import os

headers={
    "Host": "192.168.9.210",
    "Referer": "http://192.168.9.210/acmctgu/login.jsp",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

session = requests.session()
login_url = 'http://192.168.9.210/acmctgu/UserAction!login.action'
session.cookies = cookiejar.LWPCookieJar(os.environ['HOME'] + '/.ctguoj/' + ".cookies")

try:
    session.cookies.load(ignore_discard=True, ignore_expires=True)
except:
    pass
    

# 获取登录参数                                                                                                         
def get_login_data(username,password):
    #获取验证码
    #html = requests.get('http://192.168.9.210/acmctgu/UserAction!captcha.action')
    #with open('vcode.jpeg', 'wb') as file:
    #    file.write(html.content)
    #验证码识别
    #image = Image.open('vcode.jpeg')    
    image = Image.open(BytesIO(session.get('http://192.168.9.210/acmctgu/UserAction!captcha.action').content))
    vcode = pytesseract.image_to_string(image)

    data = {
        'user.username': username,
        'user.userpassword': password,
        'verifycode':vcode
    }
    return data
    

#登录
def postLogin(un,pd):
    # print u'输入用户名'.decode('utf-8').encode('gbk')                                                            
    data = get_login_data(un,pd)
    
    resp = session.post(login_url,data=data, headers=headers)
    return resp
#获取个人信息，用于判断是否登录
def getInfo():
    action = "http://192.168.9.210/acmctgu/UserAction!userInfo.action"
    resp = session.post(action,headers=headers)
    return resp
    
#获取比赛题目列表
def getContest():
    action="http://192.168.9.210/acmctgu/PaperAction/PaperAction!getPapers.action?&selectOne=&teacherOrexam=&status=&isjava=&index=1"
    resp = session.get(action,headers=headers)
    return resp

#获取题目
def getProblem(Cid,Ctype,Cpass):
    action="http://192.168.9.210/acmctgu/Exam/ExamAction!beginExam.action?id="+Cid+"&type="+Ctype
    #如果需要密码
    if Cpass == '1':
        action = "http://192.168.9.210/acmctgu/Exam/ExamAction!pwbeginExam.action?id="+ Cid+ "&type="+Ctype
    resp = session.get(action)
    return resp

#请求带密码题目
def postProblemPasswd(Cid,password):
    action = "http://192.168.9.210/acmctgu/Paper/PaperAction!checkpw.action?password="+password+"&id="+Cid
    resp = session.get(action)
    return resp

#获取所有排名列表
def getRankList():
    action  = "http://192.168.9.210/acmctgu/Exam/ExamAction!showRank.action"
    resp = session.get(action)
    return resp

#获取排名
def getRanking(id):
    action = "http://192.168.9.210/acmctgu/Exam/ExamAction!rankInfo.action?id="+id
    resp = session.get(action)
    return resp

#提交代码,返回判题信息
def getSubResp(code,Pid,Ctype):
    action = "http://192.168.9.210/acmctgu/ExamAction/CheckAction!checkAnswer.action"
    data = {
        'answer': code,
        'id': Pid,
        'type': Ctype
    }
    resp = session.post(action,data=data, headers=headers)
    return resp

#获取已通过题目信息
def getPassed(Cid):
    action = "http://192.168.9.210/acmctgu/Exam/ExamAction!paperInfo.action?id="+Cid
    resp = session.get(action,headers=headers)
    return resp

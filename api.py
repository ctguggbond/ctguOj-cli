import requests
import pytesseract 
from PIL import Image
from io import BytesIO
import termcolor
from http import cookiejar

headers={
    "Host": "192.168.9.210",
    "Referer": "http://192.168.9.210/acmctgu/login.jsp",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

session = requests.session()
login_url = 'http://192.168.9.210/acmctgu/UserAction!login.action'
session.cookies = cookiejar.LWPCookieJar("cookies")
session.cookies.load(ignore_discard=True, ignore_expires=True)


username=''
password=''


# 获取登录参数                                                                                                         
def get_login_data():
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
def postLogin():
    # print u'输入用户名'.decode('utf-8').encode('gbk')                                                                
    global username, password
    username = input(termcolor.colored(u'输入用户名: ', 'cyan'))
    password = input(termcolor.colored(u'输入密码: ', 'cyan'))
    data = get_login_data()
    
    resp = session.post(login_url,data=data, headers=headers)
    return resp

#获取比赛题目列表
def getContest():
    action="http://192.168.9.210/acmctgu/PaperAction/PaperAction!getPapers.action?&selectOne=&teacherOrexam=&status=&isjava=&index=1"
    resp = session.get(action,headers=headers)
    return resp

#获取题目
def getProblem(id):
    action="http://192.168.9.210/acmctgu/Exam/ExamAction!beginExam.action?id="+id+"&type=1"
    resp = session.get(action)
    return resp

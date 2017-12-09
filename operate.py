import os
from api import *
import json
from bs4 import BeautifulSoup
from ShowMessage import ShowMessage
from contest import Contest
from problem import Problem
from userInfo import UserInfo
import sys
import re
import getpass

#先加载保存的数据#########
#第一个参数比赛id 第二个语言类型java或c  第三个参数是否需要密码
contestInfo = ['185','0','0'] 

try:
    with open('.contestInfo.json','r') as file_object:
        contestInfo = json.load(file_object)
except:
    pass



#判断是否登录
def is_login():
    resp = getInfo()
    soup = BeautifulSoup(resp.text,"lxml")
    islogin = soup.find_all(text='用户名')

    if islogin :
        return True
    else :
        return False
    
#登录
def login():
    username = input(termcolor.colored(u'输入用户名: ', 'cyan'))
    password = getpass.getpass(termcolor.colored('输入密码： '))

    #验证码识别率较低..索性一次尝试5次
    tryloginTime = 5
    while(tryloginTime > 0):
        resp = postLogin(username,password)
        soup = BeautifulSoup(resp.text,"lxml")
        divlist = soup.find_all('div',class_ = 'user')
        
        if len(divlist) > 3:
            info = divlist[3].font.string
            if info != "验证码有误":
                ShowMessage.error(info)
                break
        else:
            ShowMessage.success("登录成功！")
            session.cookies.save(ignore_discard=True, ignore_expires=True)
            break;
        tryloginTime = tryloginTime -1
    if tryloginTime <= 0:
        ShowMessage.error("oooooops...验证码识别失败,再试试?")

#显示比赛列表flag位true 显示所有 flase仅显示正在进行的比赛
#就只显示第一页，后面也没什么用
def showContestList(flag):
    resp = getContest()
    jdata = json.loads(resp.text)
    
    datalist = jdata.get('list')
    
    for data in datalist:
        if data['status'] == 'running' or flag:
            c = Contest()
            c.Cid = data['id']
            if data['isjava'] == '1':
                c.Ctype = 'c'
            else:
                c.Ctype = 'java'
            c.title = data['papername']
            c.endTime = data['endtime']
            c.teacherName = data['teachername']
            c.problemDetail()
    print(''.join('id' + '\t' + '{:35}'.format('名称') + '语言' +
                '\t' + '结束时间' + '\t\t'+ '出题人'))

#获取题目信息
def getProblemInfo(Pid,isSimple):
    Cid = contestInfo[0] #比赛id
    Ctype = contestInfo[1]
    Cpass = contestInfo[2]
    resp = getProblem(Cid,Ctype,Cpass)
    #解析网页数据
    soup = BeautifulSoup(resp.text,"lxml")
    #仅获取题目和id
    if isSimple:
        pList = []
        allProblemDiv = soup.find_all('div',id=re.compile(r'title_\d*'))
        if not allProblemDiv :
            ShowMessage.error("比赛不可参加,使用use id重新选择比赛")
            sys.exit(0)
        for pdiv in allProblemDiv:
            p = Problem()
            p.Pid = re.sub("\D", "",pdiv['id'])
            p.title = pdiv.find('div',class_='nav').string.split('.')[1].strip()
            pList.append(p)
        return pList
    #获取详细题目信息
    else :
        pdiv = soup.find('div',id='title_'+Pid)
        if not pdiv:
            ShowMessage.error("你已经做过了或者没有该题目")
            sys.exit(0)
        p = Problem()
        p.Pid = re.sub("\D", "",pdiv['id'])
        p.title = pdiv.find('div',class_='nav').string.split('.')[1].strip()
        p.timeAndMem = pdiv.find('div',class_='common').string.strip()
        
        contentDiv = pdiv.find_all('div')
        p.content = contentDiv[3].pre.string
        p.descr_input = contentDiv[5].pre.string
        p.descr_output = contentDiv[7].pre.string
        p.ex_input = contentDiv[9].pre.string
        p.ex_output = contentDiv[11].pre.string
        p.code = ''
        return p

#显示题目摘要列表
def listProblem():
    ShowMessage.info("正在加载题目列表...")
    pList = getProblemInfo('',True)
    i = 1
    
    for p in pList:
        print(p.problemSimple(),end='\t')
        if i % 3 == 0:
            print('')
        i = i+1
    print('')

#显示题目详细信息
def showProblemDetail(Pid):
    ShowMessage.info("正在加载题目...")
    p = getProblemInfo(Pid,False)
    os.system('clear')
    print(p.problemDetail())


#获取排名列表
def getRankingList(Cid):
    resp = getRanking(Cid)
    soup = BeautifulSoup(resp.text,"lxml")
    rankingTr = soup.find_all('tr',id=re.compile('\d*'))
    if not  rankingTr:
        ShowMessage.error("没有该比赛排名...重新选择比赛")
        sys.exit(0)
    
    rList = []
    for tr in rankingTr:
        stu = UserInfo()
        td = tr.find_all('td')
        stu.rank = td[0].div.string
        stu.username = td[1].div.string
        stu.name = td[2].div.string
        stu.stuid = td[3].div.string
        stu.college = td[4].div.string
        stu.major = td[5].div.string
        stu.score = td[6].div.string
        stu.subTime = td[7].div.string
        rList.append(stu)
    return rList

#显示排名
def showRanking():
    Cid = contestInfo[0]
    ShowMessage.info("加载排名中...")
    rList = getRankingList(Cid)
    #    rList = rList.reverse()
    
    for i in range(0, len(rList))[::-1]:
        rList[i].showUserInfo()

#将当前选择的比赛id 及类型保存至文件,方便提交代码，不用选择提交类型，以及再次开始直接开始上次的位置
def saveContestInfo(Cid):
    resp = getContest()
    jdata = json.loads(resp.text)
    datalist = jdata.get('list')
    
    Ctype = '1'  #类型
    Cpass = '0'  #是否需要密码 0为不需要

    #根据比赛id查找比赛类型
    for data in datalist:
        if str(data['id']) == Cid:
            Ctype = data['isjava']
    #判断是否需要密码
    needPasswordTest = getProblem(Cid,Ctype,'0')
    soup = BeautifulSoup(needPasswordTest.text,'lxml')
    tableInfo = soup.find('table')

    if 'Struts Problem Report' in soup.title:
        ShowMessage.error('没有该比赛 -_-')
        sys.exit(0)

    #输入密码表格宽度30% ,  题目表格宽度100% 这样查找貌似快点,有待优化
    if tableInfo['width'] == '30%':
        Cpass = '1'
        passwd= input(termcolor.colored(u'你需要输入密码参加该比赛: ', 'green'))
        passwdisRight = postProblemPasswd(Cid,passwd)
        if passwdisRight.text == 'no':
            ShowMessage.error('密码错误!')
            sys.exit(0)
    info = [Cid,Ctype,Cpass]
    with open('.contestInfo.json','w') as file_object:
        json.dump(info,file_object)
    ShowMessage.info("设置比赛成功! 'list -p' 显示题目列表\n")
        
#生成代码模板
def genCode(Pid,codetype):
    ShowMessage.info('代码文件生成中...')
    p = getProblemInfo(Pid,False)

    title = p.title.split('(')[0].strip()

    code = '/*' + p.problemContent() + '*/\n\n'
    code = re.sub(r'\r','',code)
    
    ccode = '#include <stdio.h>\nint main(){\n\n    return 0;\n}'
    cppcode = '#include <iostream> \n#include <cstdio>\nusing namespace std;\nint main()\n{\n\n    return 0;\n}'
    javacode = 'import java.util.*;\n\npublic class Main{\n    public static void main(String args[]){\n\n    }\n}'
    
    suffix = '.c'
    if codetype == 'c':
        code = code + ccode
        suffix = '.c'
    elif codetype == 'c++':
        suffix = '.cpp'
        code = code + cppcode
    elif codetype == 'java':
        suffix = '.java'
        code = code + javacode
    fileName = Pid+'_' + title+suffix 
    f = open("./"+ fileName, "w")
    f.write(code)
    f.flush()
    f.close()
    ShowMessage.info('文件  [ '+ fileName+ ' ]  保存成功 :) ')

#提交代码
def submitCode(fileName):
    Pid = fileName.split('_')[0]
    if not re.match('\d+',Pid):
        ShowMessage.error("文件命名错误，以'id_‘开头")
        sys.exit(0)
    f = open(fileName, "r")
    code = f.read()
    f.close()
    resp = getSubResp(code,Pid,contestInfo[1])
    #{"id":"125","result":"Wrong Answer.","score":0,"time":"21:34:35"}
    try:
        jdata = json.loads(resp.text)
        result = jdata['result']
        score = jdata['score']
        time = jdata['time']
        #termcolor.colored(self.title, 'white')
        color = "red"
        if result == "Answer Correct.":
            color = "green"
            
        print(termcolor.colored(result,color) + '\n' +"得分："+ termcolor.colored(str(score),color) + '\n' +"提交时间："+ termcolor.colored(time,color))
    except:
        ShowMessage.error('提交错误，检查提交信息. *_*.')
#显示已经通过题目
def showPassed():
    Cid = contestInfo[0]
    resp = getPassed(Cid)
    soup = BeautifulSoup(resp.text,"lxml")
    titles = soup.find_all('div',class_='nav')
    if not titles :
        ShowMessage.error("你还没有通过此比赛的题目 :)")
        sys.exit(0)
    p = Problem()
    i = 1
    for t in titles :
        p.Pid = t.string.strip().split('.')[0]
        p.title = t.string.strip().split('.')[1]
        print(p.problemSimple(),end='\t')
        if i%3 == 0:
            print('')
        i = i+1
    print('')
#显示已通过题目详细信息
def showPassedDetail(Pid):
    Cid = contestInfo[0]
    resp = getPassed(Cid)
    soup = BeautifulSoup(resp.text,"lxml")
    p = soup.find('div',class_='nav',text=re.compile(r'.*'+Pid+'.*'))

    if not  p:
        ShowMessage.error("没有该题目...")
        sys.exit(0)
    infolist = ['title','content','descr_input','descr_output','ex_input','ex_output','code','score']
    j = 0
    problem = Problem()
    problem.Pid = ''
    problem.timeAndMem=''
    for i in range(0,31):
        s  = ''
        if p.string is not None:
            s = p.string
        elif p.pre is not None:
            s= p.pre.string
        elif p.span is not None:
            s = p.span.string
        elif p.textarea is not None:
            s = p.textarea.string
        if s is not None and s.strip() != '':
            setattr(problem,infolist[j],s.strip())
            j = j + 1
        p = p.next_sibling
    try:
        problem.code.index('输入描述')
        print(termcolor.colored(problem.code,'yellow'))
    except:
        print(problem.problemDetail())
    print(termcolor.colored(problem.score,'green'))
#if __name__ == "__main__" :
#    showPassed()
#    is_login()
#    submitCode("125_极差.cpp")
#    showProblemDetail('125')
#    genCode('125','c++')
#    showContestList(False)
#    saveContestInfo('124')
#    showRanking('185')
#    showProblemSimple('124','58')



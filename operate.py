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
import configparser
import base64

#文件保存基础路径
basePath = os.environ['HOME'] + '/.ctguoj/'
#配置初始化
conf = configparser.ConfigParser()


#初始化
def initCoj():
    if not os.path.exists(basePath):
        os.mkdir(basePath)
    if not os.path.exists(basePath + "ctguoj.conf"):
        #初始化配置信息
        conf.add_section('contest')
        conf.add_section('user')
        conf.set('contest', 'cid', '185') #设置比赛id
        conf.set('contest', 'ctype', '1') #设置比赛类型 0为java 1为cpp
        conf.set('contest', 'cpass', '0') #设置比赛是否需要密码 0为当前比赛不需要密码
        with open(basePath + 'ctguoj.conf', 'w') as fw:
            conf.write(fw)
    conf.read(basePath+'ctguoj.conf')
        
#判断是否登录 
def is_login():
    resp = getInfo()
    soup = BeautifulSoup(resp.text,"lxml")
    islogin = soup.find_all(text='用户名')
    if islogin:
        return True;
    else :
        return False

#登录
def login(isauto,username,password):
    if not isauto:
        username = input(termcolor.colored('请输入用户名: ', 'cyan'))
        password = getpass.getpass(termcolor.colored('请输入密码： ','cyan'))

    #验证码识别率较低..索性尝试5次
    tryloginTime = 5
    while(tryloginTime > 0):
        resp = postLogin(username,password)
        soup = BeautifulSoup(resp.text,"lxml")
        divlist = soup.find_all('div',class_ = 'user')
        
        if len(divlist) > 3:
            info = divlist[3].font.string
            if info != "验证码有误":
                conf.set('user', 'password', '')
                with open(basePath + 'ctguoj.conf', 'w') as fw:
                    conf.write(fw)
                ShowMessage.error(info)
                if isauto:
                    ShowMessage.info('请使用\'coj login\'手动登录')
                break
        else:
            ShowMessage.success("登录成功！")
            session.cookies.save(ignore_discard=True, ignore_expires=True)
            #如果是手动登录成功保存密码
            if not isauto:
                option = input(termcolor.colored(u'\n是否保存用户名及密码？ (yes/no) ', 'cyan'))
                if option == 'yes':
                    #保存密码
                    try:
                        conf.set('user', 'username', username)
                        #简单base64编码加密意思意思...
                        bytesString = password.encode(encoding="utf-8")
                        encodestr = base64.b64encode(bytesString)
                        conf.set('user', 'password', encodestr.decode(encoding='utf-8'))
                        with open(basePath + 'ctguoj.conf', 'w') as fw:
                            conf.write(fw)
                        ShowMessage.success('保存密码成功  :)')
                    except:
                        pass
            break
        tryloginTime = tryloginTime -1
    if tryloginTime <= 0:
        ShowMessage.error("oooops...验证码识别失败,再试试?")

#显示比赛列表flag位true 显示所有 flase仅显示正在进行的比赛
#只显示第一页，后面感觉也没什么用
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
    print(''.join(' id' + '\t' + '{:35}'.format('名称') + '语言' +
                '\t' + '结束时间' + '\t\t'+ '出题人'))

#获取题目信息
def getProblemInfo(Pid,isSimple):
    Cid = conf.get('contest','cid') #比赛id
    Ctype = conf.get('contest','ctype')
    Cpass = conf.get('contest','cpass')
    resp = getProblem(Cid,Ctype,Cpass)
    #解析网页数据
    soup = BeautifulSoup(resp.text,"lxml")
    #仅获取题目和id
    if isSimple:
        pList = []
        allProblemDiv = soup.find_all('div',id=re.compile(r'title_\d*'))
        if not allProblemDiv :
            ShowMessage.warn("题目空了，你可能已经AK了.")
            sys.exit(0)
        for pdiv in allProblemDiv:
            p = Problem()
            p.Pid = re.sub("\D", "",pdiv['id'])
            title = pdiv.find('div',class_='nav').string.split('.')[1].strip()
            tempStrs = title.split('(')
            p.score = int(re.sub("\D", "",tempStrs[len(tempStrs)-1]))
            p.title = title.split('(')[0].strip()
            pList.append(p)
        #按分数排序
        pList = sorted(pList,key=lambda pList:pList.score)  
        return pList
    #获取详细题目信息
    else :
        pdiv = soup.find('div',id='title_'+Pid)
        if not pdiv:
            ShowMessage.error("你已经AC了或者没有该题目")
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

    # 先尝试从缓存的文件中加载
    pList = []
    i = 1
    try:
        with open(basePath + 'problemList.json','r') as file_object:
            pList = json.load(file_object)
        for p in pList:
            print(p,end=' ')
            if i % 3 == 0:
                print('')
            i = i+1
        print('')
    except:
        #出错就从oj加载
        pList = getProblemInfo('',True)
        for p in pList:
            print(p.problemSimple(),end=' ')
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
    Cid = conf.get('contest','cid')
    ShowMessage.info("加载排名中...")
    rList = getRankingList(Cid)
    #    rList = rList.reverse()
    
    for i in range(0, len(rList))[::-1]:
        rList[i].showUserInfo()

#保存题目列表信息，不用每次请求
def saveProblemList():
    ShowMessage.info('正在缓存题目信息...')
    pList = getProblemInfo('',True)
    titleList = []
    for p in pList:
        titleList.append(p.problemSimple())
    try:
        with open(basePath + 'problemList.json','w') as file_object:
            json.dump(titleList ,file_object)
    except:
        pass

#将当前选择的比赛id 及类型保存至配置文件,方便提交代码，不用选择提交类型
def saveContestInfo(Cid):
    ShowMessage.info('正在获取比赛信息...')
    resp = getContest()
    jdata = json.loads(resp.text)
    datalist = jdata.get('list')
    
    Ctype = '1'  #类型 ...1代表c 0表示java
    Cpass = '0'  #是否需要密码 0为不需要

    #根据比赛id查找比赛类型
    for data in datalist:
        if str(data['id']) == Cid:
            Ctype = data['isjava']
            break
    #判断是否需要密码
    needPasswordTest = getProblem(Cid,Ctype,'0')

    #Struts Problem Report页面报错编码不是utf-8 
    if 'ISO-8859-1' in needPasswordTest.encoding:
        ShowMessage.error('没有该比赛 -_-\"')
        sys.exit(0)
    try:
        #如果不需要密码就没有这个头信息会抛异常，比之前的解析内容判断速度快，虽然不雅
        hasKeyContentLength = needPasswordTest.headers['Content-Length']
        Cpass = '1'
        passwd= input(termcolor.colored(u'你需要输入密码参加该比赛: ', 'green'))
        passwdisRight = postProblemPasswd(Cid,passwd)
        if passwdisRight.text == 'no':
            ShowMessage.error('密码错误!')
            sys.exit(0)
    except:
        pass

    #保存比赛信息
    conf.set('contest','cid',Cid)
    conf.set('contest','ctype',Ctype)
    conf.set('contest','cpass',Cpass)
    with open(basePath + 'ctguoj.conf', 'w') as fw:
        conf.write(fw)    
    saveProblemList()
    ShowMessage.info("设置比赛成功! 'coj list -p' 显示题目列表\n")
        
#生成代码模板
def genCode(Pid,codetype):
    ShowMessage.info('代码文件生成中...')
    p = getProblemInfo(Pid,False)

    title = p.title.split('(')[0].strip()

    code = '/*' + p.problemContent() + '\n*/\n\n'
    code = re.sub(r'\r','',code)
    
    ccode = '#include <stdio.h>\n\nint main(){\n\n    return 0;\n}'
    cppcode = '#include <iostream> \n\n#include <cstdio>\nusing namespace std;\nint main()\n{\n\n    return 0;\n}'
    javacode= 'import java.util.*;\n\npublic class Main{\n    public static void main(String args[]){\n\n    }\n}'
    
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
    fileName = Pid+'.' + title+suffix 
    f = open("./"+ fileName, "w")
    f.write(code)
    f.flush()
    f.close()
    ShowMessage.info('文件  [ '+ fileName+ ' ]  保存成功 :) ')

#提交代码
def submitCode(fileName):
    Pid = fileName.split('.')[0]
    if not re.match('^\d+$',Pid):
        ShowMessage.error("文件命名错误，请以'id.'开头， 例: 70.简单求和.c")
        sys.exit(0)
    try:
        f = open(fileName, "r")
    except:
        ShowMessage.error("没有找到文件.检查文件名是否有误")
        sys.exit(0)
    code = f.read()
    f.close()
    resp = getSubResp(code,Pid,conf.get('contest','ctype'))
    #{"id":"125","result":"Wrong Answer.","score":0,"time":"21:34:35"}
    try:
        jdata = json.loads(resp.text)
        result = jdata['result']
        score = jdata['score']
        time = jdata['time']
        color = "red"
        if result == "Answer Correct.":
            color = "green"
            
        print(termcolor.colored(result,color) + '\n' +"得分："+ termcolor.colored(str(score),color) + '\n' +"提交时间："+ termcolor.colored(time,color))
    except:
        ShowMessage.error('oops!提交出错了，请重新提交. *_*.')

#显示已经通过题目
def showPassed():
    Cid = conf.get('contest','cid')
    resp = getPassed(Cid)
    soup = BeautifulSoup(resp.text,"lxml")
    titles = soup.find_all('div',class_='nav')
    if not titles :
        ShowMessage.error("你还没有做过此比赛的题目 :)")
        sys.exit(0)
    p = Problem()
    i = 1
    for t in titles :
        title = t.string.strip().split('.')[1]
        tempStrs = title.split('(')
        p.score = int(re.sub("\D", "",tempStrs[len(tempStrs)-1]))
        p.title = title.split('(')[0].strip()
        p.Pid = t.string.strip().split('.')[0]
        print(p.problemSimple(),end='\t')
        if i%3 == 0:
            print('')
        i = i+1
    print('')

#显示已通过题目详细信息
def showPassedDetail(Pid):
    Cid = conf.get('contest','cid')
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



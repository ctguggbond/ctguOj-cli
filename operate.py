import os
from api import *
import json
from bs4 import BeautifulSoup
from ShowMessage import ShowMessage
from contest import Contest
from problem import Problem
from userInfo import UserInfo
import re


#先加载保存的数据#############
#比赛id以及以及使用的语言信息

contestInfo = ['185','0'] 

try:
    with open('contestInfo.json','r') as file_object:
        contestInfo = json.load(file_object)
except:
    ShowMessage.error("请先使用'ctguoj use cid'选择要参加的比赛")
    exit

############################


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
    resp = postLogin()
    soup = BeautifulSoup(resp.text,"lxml")
    divlist = soup.find_all('div',class_ = 'user')
    
    if len(divlist) > 3:
        info = divlist[3].font.string
        if info == "验证码有误":
            info = "oooooops...验证码识别失败,try it again~"
        ShowMessage.error(info)

    else:
        ShowMessage.success("登录成功！")
        session.cookies.save(ignore_discard=True, ignore_expires=True)
   
        
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
def getProblemInfo(Pid,flag):
    Cid = contestInfo[0] #比赛id
    Ctype = contestInfo[1]
    
    resp = getProblem(Cid,Ctype)
    soup = BeautifulSoup(resp.text,"lxml")
    #仅获取题目和id
    if flag:
        pList = []
        allProblemDiv = soup.find_all('div',id=re.compile(r'title_\d*'))
        for pdiv in allProblemDiv:
            p = Problem()
            p.Pid = re.sub("\D", "",pdiv['id'])
            p.title = pdiv.find('div',class_='nav').string.split('.')[1].strip()
            pList.append(p)
        return pList
    #获取详细题目信息
    else :
        pdiv = soup.find('div',id='title_'+Pid)
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
        return p

#显示题目摘要列表
def showProblemSimple():
    pList = getProblemInfo('',True)
    for p in pList:
        print(p.problemSimple())

#显示题目详细信息
def showProblemDetail(Pid):
    p = getProblemInfo(Pid,False)
    os.system('clear')
    print(p.problemDetail())


#获取排名列表
def getRankingList(Cid):
    resp = getRanking(Cid)
    soup = BeautifulSoup(resp.text,"lxml")
    rankingTr = soup.find_all('tr',id=re.compile('\d*'))

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
def showRanking(Cid):
    rList = getRankingList(Cid)
    #    rList = rList.reverse()
    for i in range(0, len(rList))[::-1]:
        rList[i].showUserInfo()

#将当前选择的比赛id 及类型保存至文件,方便提交代码，不用选择提交类型，以及再次开始直接开始上次的位置
def saveContestInfo(Cid):
    resp = getContest()
    jdata = json.loads(resp.text)
    datalist = jdata.get('list')
    
    #没想到什么优雅的办法...就先再查找一边找到类型id
    Ctype = '1'
    for data in datalist:
        if str(data['id']) == Cid:
            Ctype = data['isjava']

    info = [Cid,Ctype]
    with open('contestInfo.json','w') as file_object:
        json.dump(info,file_object)
    
        
#生成代码模板
def genCode(Pid,codetype):
    p = getProblemInfo(Pid,False)
    
    title = p.title.split('(')[0].strip()
    code = '/*' + p.problemContent() + '*/\n\n'
    code = re.sub(r'\r','',code)
    
    ccode = '#include <stdio.h>\nint main(){\n\n    return 0;\n}'
    cppcode = '#include <iostream> \n#include <cstdio>\nusing namespace std;\nint main()\n{\n    return 0;\n}'
    javacode = 'import java.util.*\n\npublic class Main(){\n    public static void main(String args[])\n\n}'
    
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
        
    f = open("./"+ Pid+'_'+title+suffix, "w")
    f.write(code)
    f.flush()
    f.close()


#提交代码
def submitCode(fileName):
    Pid = fileName.split('_')[0]
    f = open(fileName, "r")
    code = f.read()
    f.close()
    resp = getSubResp(code,Pid,contestInfo[1])
    {"id":"125","result":"Wrong Answer.","score":0,"time":"21:34:35"}
    jdata = json.loads(resp.text)
    result = jdata['result']
    score = jdata['score']
    time = jdata['time']
    #termcolor.colored(self.title, 'white')
    print(result + '\n' + str(score) + '\n' + time)
if __name__ == "__main__" :
    is_login()
#    submitCode("125_极差.cpp")
    
#    showProblemDetail('125')
#    genCode('125','c++')
#    showContestList(False)
#    saveContestInfo('124')
#    showRanking('185')
#    showProblemSimple('124','58')



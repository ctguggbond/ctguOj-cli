from api import *
import json
from bs4 import BeautifulSoup
from ShowMessage import ShowMessage
from contest import Contest
from problem import Problem
import re


#判断是否登录
def is_login():
    userInfo = session.get("http://192.168.9.210/acmctgu/UserAction!login.action")

#登录
def login():
    resp = postLogin()
    soup = BeautifulSoup(resp.text,"html.parser")
    divlist = soup.find_all('div',class_ = 'user')
    
    if len(divlist) > 3:
        info = divlist[3].font.string
        if info == "验证码有误":
            info = "oooooops...验证码识别失败,try it again~"
        ShowMessage.error(info)

    else:
        ShowMessage.success("登录成功！")
        session.cookies.save(ignore_discard=True, ignore_expires=True)
   
        
#显示比赛列表
def showContestList():
    resp = getContest()
    jdata = json.loads(resp.text)
    datalist = jdata.get('list')
    print(''.join('id' + '\t' + '{:20}'.format('比赛列表') + '语言' +
               ' ' + '结束时间' + ' '+ '出题人'))           
    for data in datalist:
        if data['status'] == 'running':
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

#显示题目信息
def showProblem(Cid,Pid,flag):
    resp = getProblem(Cid)
    soup = BeautifulSoup(resp.text,"lxml")
    

    #仅显示题目和id
    if flag:
        allProblemDiv = soup.find_all('div',id=re.compile(r'title_\d*'))
        for pdiv in allProblemDiv:
            p = Problem()
            p.Pid = re.sub("\D", "",pdiv['id'])
            p.title = pdiv.find('div',class_='nav').string.split('.')[1].strip()
            p.problemSimple()
    #显示详细题目信息
    else :
        pdiv = soup.find('div',id='title_'+Pid)
        p = Problem()
        p.Pid = re.sub("\D", "",pdiv['id'])
        p.title = pdiv.find('div',class_='nav').string.split('.')[1].strip()
        p.timeAndMem = pdiv.find('div',class_='common').string.strip()
        
        p.content = pdiv.find('div',class_='cribe').string
        p.descr_input = pdiv.find('div',class_='cribe').string
        p.descr_output = pdiv.find('div',class_='cribe').string
        p.ex_input = pdiv.find('div',class_='cribe').string
        p.ex_output = pdiv.find('div',class_='cribe').string
        p.problemDetail()
            
if __name__ == "__main__" :
    showProblem('185','62',False)


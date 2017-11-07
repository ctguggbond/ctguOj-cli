from api import *
import json
from bs4 import BeautifulSoup
from ShowMessage import ShowMessage
from contest import Contest



#判断是否登录
def is_login():
    userInfo = session.get("http://192.168.9.210/acmctgu/UserAction!login.action")

#登录
def login():
    resp = postLogin()
    soup = BeautifulSoup(resp.text,"html.parser")
    divlist = soup.find_all('div',class_ = 'user')
    
    if divlist:
        info = divlist[3].font.string
        if info == "验证码有误":
            info = "oooooops...验证码识别失败,try it again~"
        ShowMessage.error(info)

    else:
        ShowMessage.success("登录成功！")
        print(session.cookies)
        session.cookies.save(ignore_discard=True, ignore_expires=True)
   
        
#显示比赛列表
def showContestList():
    resp = getContest()
    jdata = json.loads(resp.text)
    datalist = jdata.get('list')
    
    for data in datalist:
        if data['status'] == 'running':
            c = Contest()
            c.Cid = data['id']
            c.Ctype = data['isjava']
            c.title = data['papername']
            c.endTime = data['endtime']
            c.teacherName = data['teachername']
            c.problemDetail()

#显示题目
def showProblem(id):
    resp = getProblem(id)
    jdata = json.loads(resp.text)
    
    
if __name__ == "__main__" :
    showContestList()


#!/usr/bin/env python3
import sys
import os
from operate import *

arg_len = len(sys.argv)

def list_commond():
    if arg_len == 3 or arg_len == 4:
        arg2 = sys.argv[2]
        if arg2 == "-c":
            if arg_len == 4 and sys.argv[3] == '-a':
                showContestList(True)
            else:
                showContestList(False)
            return 
        elif arg2 == "-p":
            listProblem()
            return 
    ShowMessage.error("参数错误\n")
    help_commond()
        
def use_commond():
    if arg_len == 3:
        arg2 = sys.argv[2]
        if re.match('\d',arg2):
            saveContestInfo(arg2)
            return
    ShowMessage.error("参数错误")
    help_commond()

def show_commond():
    if arg_len == 3:
        arg2 = sys.argv[2]
        if re.match('\d+',arg2):
            showProblemDetail(arg2)
            return
        elif arg2 == "ranking" :
            showRanking()
            return
    elif arg_len == 5:
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
        arg4 = sys.argv[4]
        if re.match('\d+',arg2) and arg3 == '-g' and re.match(r'^(java|c|c\+\+)$',arg4):
            showProblemDetail(arg2)
            genCode(arg2,arg4)
            return
    ShowMessage.error("参数错误")
    help_commond()
def submit_commond():
    if arg_len == 3:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        if arg1 == "submit":
            submitCode(arg2)
            return
    ShowMessage.error("参数错误")
    help_commond()
def passed():
    if arg_len == 2:
        showPassed()
        return
    elif arg_len == 3 and re.match('\d+',sys.argv[2]):
        showPassedDetail(sys.argv[2])
        return
    ShowMessage.error("参数错误")
    help_commond()
def help_commond():
#    os.system("clear")
    info  = "\n" \
            "-----------------------help-----------------------" \
            "\n" \
            " ctguoj list -c          | 列出所有正在进行的比赛\n" \
            " ctguoj use id           | 根据id选择比赛\n" \
            " ctguoj list -p          | 列出当前比赛题目\n" \
            " ctguoj list -c -a       | 列出所有进行和已结束的比赛\n" \
            " ctguoj show id          | 显示id对应题目的详细信息\n" \
            " ctguoj show id -g c     | 显示题目信息并生成c语言代码文件 可选参数c++ java\n" \
            " ctguoj submit filename  | 提交代码文件判题\n" \
            " ctguoj show ranking     | 显示当前参加比赛对应的排名\n" \
            " ctguoj passed           | 显示已提交过的题目列表\n" \
            " ctguoj passed id        | 显示已提交题目详细信息\n" \
            " ctguoj login            | 登录\n" \
            " ctguoj help             | 显示此帮助信息\n" \
            "--------------------------------------------------\n"
    ShowMessage.info(info)
    
def main():
    if not os.path.exists(".cookies"):
        ShowMessage.error("登录失效，请先登录.")
        login()
    elif not is_login():
        ShowMessage.error("登录失效，请先登录.")
        login()
    else:
        if arg_len < 2:
            ShowMessage.error("参数错误")
            help_commond()
            return 
        arg1 = sys.argv[1]
        if arg1 == "list":
            list_commond()
        elif arg1 == "show":
            show_commond()
        elif arg1 == "use":
            use_commond()
            ShowMessage.info("设置比赛成功! 'ctguoj list -p' 显示题目列表\n")
        elif arg1 == "submit":
            submit_commond()
        elif arg1 == "help":
            help_commond()
        elif arg1 == "login":
            login()
        elif arg1 == "passed":
            passed();
        else :
            ShowMessage.error("参数错误")
            help_commond()
            
if __name__ == '__main__':
    main()

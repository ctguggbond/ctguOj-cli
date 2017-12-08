# python大作业

用了leetcode-cli感觉很丝滑，做一个ctguoj的命令行版，虽然用处不大...
用处：可以看提交过的代码.  通过老师服务器外网可以刷题.

## env
- python3,centos7


## Install
- 安装依赖库,克隆项目，创建符号链接.

例：

```
#安装依赖库
pip3 install -r requirements.txt

git clone https://github.com/ctguggbond/ctguOj-cli.git
cd ctguOj-cli 
sudo ln -s ./ctguoj.py /usr/bin/ctguoj 
```

***
## Start：

```
ctguoj list -c   #显示进行的比赛列表
ctguoj use 185   #参加id为185的比赛
ctguoj list -p	 #显示参加比赛的题目列表
ctguoj show 124 -g java  显示id为124的题目信息并生成代码文件
ctguoj submit filename 提交代码文件判题
```

- ctguoj help显示更多帮助信息：

```
          ctguoj list -c          | 列出所有正在进行的比赛
          ctguoj use id           | 根据cid选择比赛
          ctguoj list -p          | 列出当前比赛题目
          ctguoj list -c -a       | 列出所有进行和已结束的比赛
          ctguoj show id          | 显示id对应题目的详细信息
          ctguoj show id -g c     | 显示题目信息并生成c语言代码文件
          ctguoj submit filename  | 提交代码文件判题
          ctguoj show ranking     | 显示当前参加比赛对应的排名
	  ctguoj passed           | 显示已提交的题目列表
          ctguoj passed id        | 显示所有已提交题目详细信息
	  ctguoj login            | 登录
          ctguoj help             | 显示此帮助信息
```

***

## 外部依赖函数库
- leptonica-devel  安装tesseract-orc的时候需要这个函数库
还需要这几个图片库libgif libjpeg libpng libtiff zlib，lepptonica 借用他们解析图片

***


#### ...
- 中英文字符串对齐最终解决方案：'{:<{l}}'.format(text),l= 50-len(text.encode('GBK'))+len(text))
- 控制台参数接收可以改成 ArgumentParser.  开始不知道，暴力了一堆if else,不错好像显示效果更好看...
- 安装tesseract可能会包leptonica.h not found 错误，可以参考  [编译安装tesseract](http://www.ggbond.cc/编译安装tesseract )




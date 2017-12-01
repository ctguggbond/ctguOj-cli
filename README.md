# python大作业



用了leetcode-cli感觉很丝滑，做一个ctguoj的命令行版，虽然用处不大...

- 克隆项目，在一个path目录中创建符号链接.
例：

> git clone https://github.com/ctguggbond/ctguOj-cli.git
cd ctguOj-cli 
sudo ln -s ./ctguoj.py /usr/bin/ctguoj 


- 要使用还要解决后面一堆依赖库


***
# 开始使用：

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
          ctguoj passed id        | 显示已提交题目详细信息
	  ctguoj login            | 登录
          ctguoj help             | 显示此帮助信息
```
***

#### 使用的库

- tesseract安装可以看  [编译安装tesseract](http://www.ggbond.cc/编译安装tesseract )
其他的用pip3 install 都能解决

- requsts

#### html解析

- bs4 

- lxml#开始用自带的htmlparser 死活找不全。。我还以为方法错了

#### 验证码识别
- pillow  python3PIL图像处理库

- pytesseract Python-tesseract 是光学字符识别Tesseract OCR引擎的Python封装类(不知道是什么)

- tesseract-ocr google的ocr识别引擎

- leptonica-devel  编译tesseract-orc的时候需要这个函数库
这几个图片库也要装上lepptonica 借用他们解析图片libgif libjpeg libpng libtiff zlib


- termcolor 终端颜色显示

***


#### issue
- 登录后会在当前目录创建.cookies 保存登录状态 和.contestInfo保存一些必要的信息.
中英文字符串对齐最终靠谱解决方案：'{:<{l}}'.format(text),l= 50-len(text.encode('GBK'))+len(text))

- 控制台参数接收可以改成 ArgumentParser.  开始不知道，暴力了一堆if else



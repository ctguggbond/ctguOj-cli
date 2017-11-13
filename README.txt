python大作业
用了leetcode-cli感觉很丝滑，做一个ctguoj的命令行版，虽然用处不大...

把项目克隆下来，在一个path目录中创建符号链接.
例：
git clone https://git.ctguqmx.com/ggbond/ctguOj-cli.git
cd ctguOj-cli 

sudo ln -s ./ctguoj.py /usr/bin/ctguoj 或 mkdir ~/bin; ln -s ./ctguoj.py ~/bin/ctguoj



开始使用：
----------------------------------------------------------
ctguoj list -c   #显示进行的比赛列表
ctguoj use 185   #参加id为185的比赛
ctguoj list -p	 #显示参加比赛的题目列表
ctguoj show 124 -g java  显示id为124的题目信息并生成代码文件
ctguoj submit filename 提交代码文件判题
-----------------------------------------------------------


ctguoj help显示更多帮助信息：

          ctguoj list -c          | 列出所有正在进行的比赛" 
          ctguoj use id           | 根据cid选择比赛" 
          ctguoj list -p          | 列出当前比赛题目" 
          ctguoj list -c -a       | 列出所有进行和已结束的比赛" 
          ctguoj show id          | 显示id对应题目的详细信息" 
          ctguoj show id -g c     | 显示题目信息并生成c语言代码文件" 
          ctguoj submit filename  | 提交代码文件判题" 
          ctguoj show ranking     | 显示当前参加比赛对应的排名" 
          ctguoj help             | 显示此帮助信息" 


#####使用的库#####
requsts

#html解析
bs4 
lxml#开始用自带的htmlparser 死活找不全。。我还以为方法错了

#验证码识别
pillow  python3PIL图像处理库
tesseract-ocr google的ocr识别引擎
pytesseract Python-tesseract 是光学字符识别Tesseract OCR引擎的Python封装类(不知道是什么)
leptonica-devel  编译tesseract-orc的时候需要这个函数库

termcolor 终端颜色显示

---------------
登录后会在当前目录创建.cookies 保存登录状态 和.contestInfo保存一些必要的信息.
中英文字符串对齐最终靠谱解决方案：'{:<{l}}'.format(text),l= 50-len(text.encode('GBK'))+len(text))

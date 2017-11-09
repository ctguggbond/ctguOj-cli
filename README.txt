python大作业
用了leetcode-cli感觉很丝滑，做一个ctguoj的命令行版，虽然用处不大...



#使用的库
requsts
#html解析
bs4 

#验证码识别
pillow 
tesseract-ocr
leptonica-devel

#html解析
lxml#开始用自带的htmlparser 死活找不全。。我还以为方法错了


中英文字符串对齐最终靠谱解决方案：'{:<{l}}'.format(text),l= 50-len(text.encode('GBK'))+len(text))

python大作业
用了leetcode-cli感觉很丝滑，做一个ctguoj的命令行版，虽然用处不大...



#使用的库
requsts
#html解析
bs4 

#验证码识别
pillow  python3PIL图像处理库
tesseract-ocr google的ocr识别引擎
pytesseract Python-tesseract 是光学字符识别Tesseract OCR引擎的Python封装类(不知道是什么)

leptonica-devel  编译tesseract-orc的时候需要这个函数库

#html解析
lxml#开始用自带的htmlparser 死活找不全。。我还以为方法错了


中英文字符串对齐最终靠谱解决方案：'{:<{l}}'.format(text),l= 50-len(text.encode('GBK'))+len(text))

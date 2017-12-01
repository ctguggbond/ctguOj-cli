import termcolor

class Problem:
            
    def __init__(self):
          pass
    def problemDetail(self):
        Pid = termcolor.colored(self.Pid, 'magenta')
        title = termcolor.colored(self.title, 'white')
        timeAndMem = termcolor.colored("(" + self.timeAndMem + ")", 'green')
        content = termcolor.colored(self.content, 'white')
        descr_input = termcolor.colored(self.descr_input, 'white')
        descr_output = termcolor.colored(self.descr_output, 'white')
        ex_input = termcolor.colored(self.ex_input, 'white')
        ex_output = termcolor.colored(self.ex_output, 'white')
        code = termcolor.colored(self.code, 'yellow')
        info1 = termcolor.colored('题目内容:','magenta')
        info2 = termcolor.colored('输入描述:','magenta')
        info3 = termcolor.colored('输出描述:','magenta')
        info4 = termcolor.colored('输入样例:','magenta')
        info5 = termcolor.colored('输出样例:','magenta')
        
        info = '\n'.join(['Id:['+Pid + ']' + '\t\t' + title,timeAndMem,info1,content,info2,descr_input,info3,descr_output,info4,ex_input,info5,ex_output,code])
        return '\n\n' + info
        
    def problemSimple(self):
        Pid = termcolor.colored(self.Pid, 'magenta')
        title = termcolor.colored(self.title, 'white')
        simpleInfo = ''.join('[' + Pid + ']' + '-' + title)
        return '{:<{l}}'.format(simpleInfo,l= 30-len(title.encode('GBK'))+len(simpleInfo)) 
        
    def problemContent(self):
        info1 = '题目内容:'
        info2 = '输入描述:'
        info3 = '输出描述:'
        info4 = '输入样例:'
        info5 = '输出样例:'
        
        info = '\n'.join(['Id:['+self.Pid + ']' + '\t',self.title,self.timeAndMem,info1,self.content,info2,self.descr_input,info3,self.descr_output,info4,self.ex_input,info5,self.ex_output])
        return '\n' + info

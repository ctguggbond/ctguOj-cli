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
        info = '\n'.join([Pid + '\t\t' + title,timeAndMem, content,descr_input,descr_output,ex_input,ex_output]) + '\n'
        print(info)
    def problemSimple(self):
        Pid = termcolor.colored(self.Pid, 'magenta')
        title = termcolor.colored(self.title, 'white')
        simpleInfo = ''.join('[' + Pid + ']' + '\t' + title)
        print(simpleInfo)

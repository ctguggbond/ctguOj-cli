
class Problem:
            
    def __init__(self):
          pass
    problemDetail():
        Pid = termcolor.colored(topic.Pid, 'yellow')
        title = termcolor.colored(topic.title, 'white')
        timeAndMem = termcolor.colored("(" + topic.timeAndMem + ")", 'green')
        content = termcolor.colored(topic.content, 'magenta')
        descr_input = termcolor.colored(topic.descr_input, 'white')
        descr_output = termcolor.colored(topic.descr_output, 'white')
        ex_input = termcolor.colored(topic.ex_input, 'white')
        ex_output = termcolor.colored(topic.ex_output, 'white')
        info = '\n'.join([Pid + '\t\t' + title,timeAndMem, content,desc_input,desc_output,ex_input,ex_output]) + '\n'
        print(info)
    problemSimple():
        Pid = termcolor.colored(topic.Pid, 'yellow')
        title = termcolor.colored(topic.title, 'white')
        simpleInfo = ''.josin([Pid + '\t\t' + title])
        print(simpleInfo)

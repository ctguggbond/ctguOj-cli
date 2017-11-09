import termcolor

class Contest:

    def __init__(self):
          pass

    def problemDetail(self):
        Cid = termcolor.colored(self.Cid, 'magenta')
        title = termcolor.colored(self.title, 'white')
        Ctype = termcolor.colored(self.Ctype, 'blue')
        endTime = termcolor.colored("(" + self.endTime + ")", 'red')
        teacherName = termcolor.colored(self.teacherName, 'red')
        info = '\n'.join(['['+Cid + ']' + ' ' + '{:<{l}}'.format(title,l= 50-len(title.encode('GBK'))+len(title)) + Ctype + '\t' + endTime + ' '+ teacherName])
        print(info)

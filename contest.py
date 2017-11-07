import termcolor

class Contest:

    def __init__(self):
          pass

    def problemDetail(self):
        Cid = termcolor.colored(self.Cid, 'yellow')
        title = termcolor.colored(self.title, 'white')
        Ctype = termcolor.colored(self.Ctype, 'blue')
        endTime = termcolor.colored("(" + self.endTime + ")", 'green')
        teacherName = termcolor.colored(self.teacherName, 'red')
        info = '\n'.join([Cid + '\t' + ' '+  title + '\t\t' + Ctype + ' ' + endTime + ' '+ teacherName])
        print(info)

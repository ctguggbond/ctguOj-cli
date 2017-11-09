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
        info = '\n'.join(['['+Cid + ']' + ' ' + '{:30}'.format(title) + Ctype + ' ' + endTime + ' '+ teacherName])
        print(info)

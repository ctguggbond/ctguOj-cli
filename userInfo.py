import termcolor

class UserInfo:
    def __init__(self):
        pass
    
    def showUserInfo(self):
        rank = termcolor.colored(self.rank, 'magenta')
        rank = '{:<10}'.format(rank)
        username = termcolor.colored(self.username, 'white')
        username = '{:<{l}}'.format(username,l= 28-len(username.encode('GBK'))+len(username))
        name = termcolor.colored(self.name, 'green')
        name  = '{:<{l}}'.format(name,l= 15-len(name.encode('GBK'))+len(name))
        
        stuid = termcolor.colored(self.stuid, 'magenta')
        stuid =  '{:<{l}}'.format(stuid,l = 15-len(stuid.encode('GBK'))+len(stuid))

        college =termcolor.colored(self.college, 'yellow')
        college = '{:<{l}}'.format(college,l= 35-len(college.encode('GBK'))+len(college))

        major =termcolor.colored(self.major, 'blue')
        major = '{:<{l}}'.format(major,l= 30-len(major.encode('GBK'))+len(major))
        
        score = termcolor.colored(self.score, 'red')
        subTime = termcolor.colored(self.subTime, 'cyan')
        
        info = ''.join(rank + ' ' + username+' ' + name + ' ' + stuid+ ' '+ college + ' ' + major + ' ' + score)
        print(info)
        

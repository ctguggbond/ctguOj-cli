import termcolor

class ShowMessage:                                                                                                
    flag = True

    @staticmethod
    def error(msg):
        if ShowMessage.flag:
            print ("".join([termcolor.colored("ERROR", "red"), ": ", termcolor.colored(msg, "white")]))
            
    @staticmethod
    def warn(msg):
        if ShowMessage.flag:
            print ("".join([termcolor.colored("WARN", "yellow"), ": ", termcolor.colored(msg, "white")]))
            
    @staticmethod
    def info(msg):
        if ShowMessage.flag:
            print (termcolor.colored(msg, "green"))
            
    @staticmethod
    def debug(msg):
        if ShowMessage.flag:
            print ("".join([termcolor.colored("DEBUG", "magenta"), ": ", termcolor.colored(msg, "white")]))

    @staticmethod
    def success(msg):
        if ShowMessage.flag:
            print ("".join([termcolor.colored("SUCCESS", "green"), ": ", termcolor.colored(msg, "white")]))

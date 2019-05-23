import Modules.RDP as RDP
import Modules.Reply as Reply
import Modules.String as String
import Modules.Math as Math
import Modules.File as File
import Modules.Log as Log
import Modules.Web as Web
#!!#

class LineOfCode(object):
    def __init__(self, contents, authorizedModules=[]):
        self.raw = contents
        cmds = contents.strip(" ").split("|")
        self.child = None
        if len(cmds) > 1:
            self.child = LineOfCode("|".join(cmds[1:]), authorizedModules)
        self.function = cmds[0].split(" ")[0]
        self.arguments = ",".join(self.grabRefs(cmds[0].split(" ")[1:]))
        self.auth = False
        if len(authorizedModules) > 0:
            self.auth = self.function.split(".")[0] in authorizedModules
        

    def evaluate(self, vars):
        if self.auth:
            print(f"{self.function}")
            out = eval(f"{self.function}(vars, {self.arguments})")
            if self.child != None:
                self.child.arguments = ",".join([out, self.child.arguments])
                return self.child.evaluate(vars)
            return True
        else:
            print(f"Unauthroized command {self.function}")
            return False

    @staticmethod
    def grabRefs(arguments):
        newArgList = []
        inString = False
        string = ""
        for arg in arguments:
            if len(arg) > 0:
                if arg[0] == "$":
                    newArgList.append(f"vars['{arg[1:]}']")
                else:
                    if not inString:
                        if arg[0] == '"' or arg[0] == "'":
                            inString = True
                            string = ""
                        else:
                            newArgList.append(arg)
                    if inString:
                        string = string + arg + " "
                        if arg[-1] == "'" or arg[-1] == '"':
                            inString = False
                            newArgList.append(string.strip(" "))        
        return newArgList


class Script(object):
    def __init__(self, cmdlet, AllowedModules=[]):
        self.cmdlet = cmdlet

        self.variables = None
        self.lines = [LineOfCode(x, AllowedModules) for x in self.cmdlet.extractCommands()]
        self.parserPos = 0
        self.AllowedModules = AllowedModules


    def initialize(self, environment):
        self.variables = self.cmdlet.extractVariables()
        self.variables["LOG"] = ""
        if "RDP" in self.AllowedModules:
            self.variables["MOUSEX"] = 0
            self.variables["MOUSEY"] = 0
            self.variables["PRESSEDKEYS"] = []
        if "Reply" in self.AllowedModules:
            self.variables["MAILCONTROLLER"] = environment
            self.variables["SENDER"] = self.cmdlet.respondTo
            self.variables["SUBJECT"] = self.cmdlet.tag
            self.variables["MailBody"] = ""
            self.variables["BODY"] = ""

    def execute(self):
        for line in self.lines:
            line.evaluate(self.variables)
from os import listdir
from os.path import isfile, join


class Script(object):
    def __init__(self, filename):
        with open("./Scripts/"+filename, "r") as file:
            self.lines = file.readlines()
        self.name = filename[:-4]
        self.exLines = None

    def setVariables(self, var):
        self.exLines = []
        for i in self.lines:
            self.exLines.append(eval(f'f"""{i}"""'))
    
    def Load(self, vars={}):
        if self.exLines != None:
            stringRep = ""
            for line in self.exLines:
                stringRep = stringRep + line.strip("\n") + "\n"
            return stringRep
        if self.exLines == None:
            self.setVariables({})
            return self.Load()
        return None

class DynamicScript(Script):
    def __init__(self, name):
        self.name = name
        self.lines = []
        self.exLines = None

    def addLine(self, line):
        self.lines.append(line)

    def writeToFile(self):
        with open(f"./Scripts/{self.name}.ess") as file:
            file.writelines(self.lines)


class ScriptLoader(object):
    def __init__(self):
        self.scripts = []
        path = "./Scripts/"
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        scripts = [f for f in onlyfiles if f[-4:].lower() == ".ess"]
        for scriptName in scripts:
            self.scripts.append(Script(scriptName))

    def getScript(self, name):
        for s in self.scripts:
            if name.lower() == s.name.lower():
                return s

    def CreateDynamicScript(self, name="NEWESS"):
        DS = DynamicScript(name)
from os import listdir
from os.path import isfile, join

def getModules(path="./Server/src/Modules"):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    pythonModules = [x[:-3] for x in onlyfiles if x[-3:] == ".py"]
    return pythonModules

def writeModules(filename, modules, ident="#!!#",path="./Server/src/"):
    with open(path+filename, "r") as file:
        script = file.readlines()
    newScript = []
    writing = False
    for line in script:
        if len(line) >= len(ident):
            if line[:len(ident)] == ident:
                writing = True
        if writing:
            newScript.append(line)
    
    for mod in modules:
        newScript.insert(0, f"import Modules.{mod} as {mod}\n")

    with open(path+filename, "w+") as file:
        file.writelines(newScript)
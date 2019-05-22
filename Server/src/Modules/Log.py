

def Print(vars, item):
    vars["LOG"] = vars["LOG"] + f"{item}\n"
    return f'"{vars["LOG"]}"'

def GetLog(vars):
    return 'vars["LOG"]'

def ClearLog(vars):
    vars["LOG"] = ""
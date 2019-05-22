

def Attach(vars, filename=""):
    print(f"Attaching file {filename}")
    return True or False

def Body(vars, content):
    vars["BODY"] = vars["BODY"] + f"{content}\n"
    return f'"{vars["BODY"]}"'

def ClearBody(vars):
    vars["BODY"] = ""

def SendReply(vars):
    body = vars["BODY"]
    controller = vars["MAILCONTROLLER"]
    sender = vars["SENDER"]
    subject = vars["SUBJECT"]
    controller.sendMail(sender, f"SERVICE OUTPUT", body)

def SendReplyVar(vars, variable):
    SendReply(vars, vars[variable])
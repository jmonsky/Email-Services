class Cmdlet(object):

    def __init__(self, mail):
        self.respondTo = mail.sender
        self.tag = mail.subject

        self.commands = [l[1:] for l in str(mail.message).split("\n") if len(l) > 0 and l[0] == "`"]
        self.data = [x[1:] for x in str(mail.message).split("\n") if len(x) > 0 and x[0] == "~"]

    def extractCommands(self):
        return self.commands

    def extractVariables(self):
        variables = dict()
        for i in self.data:
            if len(i.split("=")) == 2:
                name, value = i.split("=")
                variables[name.strip(" ")] = value.strip(" ")
        return variables
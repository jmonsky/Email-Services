import importlib
from time import sleep

import ModuleLoader
loadableMods = ModuleLoader.getModules()
ModuleLoader.writeModules("script.py", loadableMods)

from mailController import MailController
from Command import Cmdlet
import script

with open("server_config.txt", "r") as file:
    clist = [x.split(":") for x in file.readlines()]
    config = dict()
    for option in clist:
        config[option[0]] = option[1].strip("\n")
    del clist

c = MailController()
c.login(config["USERNAME"], config["PASSWORD"], config["SMTP_ADDRESS"], config["IMAP_ADDRESS"], int(config["SMTP_PORT"]), int(config["IMAP_PORT"]))
print("Logged In")
AllowedModules = [x.strip(" ") for x in config["ALLOWED_MODULES"].split(",")]
run = True
while run:
    for m in c.getMail():
        if m.subject == "SERVICE INPUT":
            cmd = Cmdlet(m)
            s = script.Script(cmd, AllowedModules)
            s.initialize(c)
            s.execute()
            c.delMail(m)
        if m.subject == "SERVICE SHUTDOWN":
            run = False
            c.delMail(m)
    sleep(1)

c.disconnect()
print("Done")
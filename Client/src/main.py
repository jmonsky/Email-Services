from time import time
import sys
import getpass

import pygame
from pygame.locals import *

from mouse import Mouse
import Modules.ScriptLoader as SL
from mailController import MailController
from Modules.File import StandardDeSerialize, StandardSerialize
from Modules.screencap import ScreenCap
from button import Button

def setIcon(R, G, B):
    icon = pygame.Surface((32, 32))
    icon.fill((R,G,B))
    pygame.display.set_icon(icon)

def blitText(surface, text, pos, color=(0,0,0), textSize=15, font="Arial"):
    surface.blit(pygame.font.SysFont(font, textSize).render(text, True, color), pos)

def keyPressed(key, unicode):
    pass

def keyHeld(key, unidcode, time):
    pass

def mousePressed(x, y, button):
    pass

def mouseReleased(x, y, button):
    pass

def switchMenu(m):
    global MENU, MENUS
    print(m, len(MENUS))
    if m > len(MENUS)-1:
        m = len(MENUS)-1
    if m < 0:
        m = 0
    MENU = m
    for x in range(len(MENUS)):
        MENUS[x].NoSelect()
        if x == m:
            MENUS[x].Selected()

def createSwitch(x):
    global switchMenu
    def switchTo():
        switchMenu(x)

    return switchTo

def ToggleMacro():
    global BUTTONS, SC, RECORDING, RCSCRIPT, RCTIME, server_address, MC
    for button in BUTTONS[MENU]:
        if button.name == "Start Rec":
            RCSCRIPT = SL.DynamicScript("Recording Script")
            button.name = "Stop Rec"
            RCTIME = time()
            RECORDING = True
            print("STARTING RECORDING")
            break
        elif button.name == "Stop Rec":
            button.name = "Start Rec"
            RCSCRIPT.writeToFile()
            MC.sendMail(server_address, "SERVICE INPUT", RCSCRIPT.Load())
            RECORDING = False
            print("STOPPING RECORDING")
            #del RCSCRIPT
            break

def mouseClicked(x, y, button):
    global RCTIME
    if y < MENUBARHEIGHT:
        X = 0
        for button in MENUS:
            if x > X and x < button.length + X:
                button.Click()
                FUNCQ.append(button)
            X = X + button.length + 10
    if y > MENUBARHEIGHT and y < MENUBARHEIGHT + BBARHEIGHT:
        X = 0
        for button in BUTTONS[MENU]:
            if x > X and x < button.length + X:
                button.Click()
                FUNCQ.append(button)
            X = X + button.length + 10
    if y > MENUBARHEIGHT + BBARHEIGHT:
        ay = y - MENUBARHEIGHT - BBARHEIGHT
        factor = SETTINGS["Monitor"] - 1
        if SETTINGS["ReverseMonitor"]:
            factor = SETTINGS["Monitors"] - SETTINGS["Monitor"]
        ax = x + xS * factor
        awidth = width
        aheight = y - MENUBARHEIGHT - BBARHEIGHT

        if MENUS[MENU].name == "Remote Control":
            if RECORDING and RCSCRIPT != None:
                if button == 1:
                    if len(RCSCRIPT.lines) > 0 and abs(time() - RCTIME) < 0.5:
                        RCSCRIPT.addLine(f"`RDP.Sleep {abs(time() - RCTIME)}")
                        RCTIME = time()
                    RCSCRIPT.addLine(f"`RDP.ClickAt {(ax / width) * xS} {(ay / (height - MENUBARHEIGHT - BBARHEIGHT)) * yS}")
                elif button == 3:
                    if len(RCSCRIPT.lines) > 0 and abs(time() - RCTIME) < 0.5:
                        RCSCRIPT.addLine(f"`RDP.Sleep {abs(time() - RCTIME)}")
                        RCTIME = time()
                    RCSCRIPT.addLine(f"`RDP.RightClickAt {(ax / width) * xS} {(ay / (height - MENUBARHEIGHT - BBARHEIGHT)) * yS}")

def mouseDragged(drag, button):
    pass

def mouseMoved(x,y,dx,dy, button):
    pass

def nextMon():
    global SETTINGS
    m = SETTINGS["Monitor"]
    m = m + 1
    if m > SETTINGS["Monitors"]:
        m = SETTINGS["Monitors"]
    SETTINGS["Monitor"] = m
def prevMon():
    global SETTINGS
    m = SETTINGS["Monitor"]
    m = m - 1
    if m < 1:
        m = 1
    SETTINGS["Monitor"] = m

def toggleRev():
    global SETTINGS
    SETTINGS["ReverseMonitor"] = not SETTINGS["ReverseMonitor"]

def preInit():
    global MENUS, MENU, BUTTONS, BBARHEIGHT, MENUBARHEIGHT, FUNCQ, RECORDING, RCSCRIPT, RCTIME, SETTINGS
    SETTINGS = {
        "Monitor":1,
        "Monitors":1,
        "ReverseMonitor":False,
    }
    RCSCRIPT = None
    RCTIME = 0
    BBARHEIGHT = 50
    MENUBARHEIGHT = 25
    MENUS = [
        Button("Remote Control"), 
        Button("Web"), 
        Button("File Browser"),
        Button("Settings")
        ]
    MENU = 0
    BUTTONS = [
        [Button("Quit", function=Exit), Button("Update", function=udpateMail), Button("Screen Shot", function=RequestScreenShot), Button("Start Rec", function=ToggleMacro)], 
        [Button("Quit", function=Exit),], 
        [Button("Quit", function=Exit),],
        [
            Button("Quit", function=Exit),
            Button("Update", function=udpateMail),
            Button("Request Screen Data", function=getScreenData),
            Button("Prev Monitor", function=prevMon),
            Button("Next Monitor", function=nextMon),
            Button("Reverse Monitor", function=toggleRev)]
        ]
    
    FUNCQ = []
    RECORDING = False
    for x,button in enumerate(MENUS):
        button.buttonHeight = MENUBARHEIGHT - 5
        button.function = createSwitch(x)
        button.color = (180, 180, 180)
    MENUS[0].Selected()

    for bList in BUTTONS:
        for button in bList:
            button.buttonHeight = BBARHEIGHT

    global MC, server_address, SC
    with open("client_config.txt", "r") as file:
        clist = [x.split(":") for x in file.readlines() if len(x.strip("\n")) > 0]
        config = dict()
        for option in clist:
            config[option[0]] = option[1].strip("\n")
        del clist
    if "USERNAME" in config.keys():
        print(f"Username {config['USERNAME']} in config file")
        username = config["USERNAME"]
    else:
        username = input("Email: ")
    if "PASSWORD" in config.keys():
        print("Password found in config file")
        password = config["PASSWORD"]
    else:
        if "USERNAME" in config.keys():
            print("No password found in config file")
        password = getpass.getpass()
    MC = MailController()
    
    server_address = config["SERVER_ADDRESS"]
    MC.login(username, password,  config["SMTP_ADDRESS"], config["IMAP_ADDRESS"], int(config["SMTP_PORT"]), int(config["IMAP_PORT"]))

    SC = SL.ScriptLoader()
    for m in MC.getMail():
        if m.subject == "SERVICE OUTPUT":
            MC.delMail(m)

def getScreenData():
    startupScript = SC.getScript("GetScreenData")
    startupScript.setVariables({})
    MC.sendMail(server_address, "SERVICE INPUT", startupScript.Load())

def postInit():
    global xS, yS
    global ScreenCaps
    for m in MC.getMail():
        break
        if m.subject == "SERVICE OUTPUT":
            MC.delMail(m)
    getScreenData()

    ScreenCaps = []

    xS = 1920  
    yS = 1080

def run(dt):
    global ScreenCaps, FUNCQ
    ScreenCaps = [x.update() for x in ScreenCaps]
    for item in FUNCQ:
        if type(item) == Button:
            item.execute()
    FUNCQ = []

def udpateMail():
    global xS, yS
    global ScreenCaps
    global SETTINGS
    print(f"Getting Mail {time()}")
    for m in MC.getMail():
        if m.subject == "SERVICE OUTPUT":
            for line in str(m.message).split("\n"):
                if line[:2] == f"%%":
                    print(line[:5])
                    args = line.split(" ")
                    if "Resolution" in args:
                        xS = int(args[3][:-1])
                        yS = int(args[4])
                    if "Monitors" in args:
                        SETTINGS["Monitors"] = int(args[3])
                    if args[2] == "-":
                        print("File Found!")
                        filename = StandardDeSerialize(None, line)
                        for sc in ScreenCaps:
                            if sc.exists(filename):
                                break
                        else:
                            ScreenCaps.append(ScreenCap(filename))
                    MC.delMail(m)

def RequestScreenShot():
    global SETTINGS
    screenshotScript = SC.getScript("ScreenShot")
    screenshotScript.setVariables(SETTINGS)
    MC.sendMail(server_address, "SERVICE INPUT", screenshotScript.Load())
    print("Requesting screenshot")

def Exit():
    MC.disconnect()
    pygame.quit()
    sys.exit()

def draw(surface, dt):
    surface.fill((255, 255, 255))

    MenuBar = pygame.Surface((width, MENUBARHEIGHT))
    ButtonBar = pygame.Surface((width, BBARHEIGHT))
    TotalHeight = MENUBARHEIGHT + BBARHEIGHT

    MenuBar.fill((255,255,255))
    ButtonBar.fill((200,200,200))

    x = 0
    for button in MENUS:
        s = button.CreateSurf()
        MenuBar.blit(s, (x, 0))
        x = x + button.length + 10


    x = 0
    for button in BUTTONS[MENU]:
        s = button.CreateSurf()
        ButtonBar.blit(s, (x, 0))
        x = x + button.length + 10

    if MENUS[MENU].name == "Remote Control":
        for s in ScreenCaps:
            s.scale(width, height-TotalHeight)
            i = s.getPicture()
            surface.blit(i,(s.Position[0],TotalHeight+s.Position[1]))
    
    if MENUS[MENU].name == "Settings":
        settingTexts = []
        for S in SETTINGS.keys():
            settingTexts.append(f"{S} : {SETTINGS[S]}")
        y = 1
        for t in settingTexts:
            blitText(surface, t, (20, y * 40 + TotalHeight), textSize=30)
            y += 1

    surface.blit(MenuBar, (0,0))
    surface.blit(ButtonBar, (0, MENUBARHEIGHT))
    return surface


if __name__ == "__main__":
    preInit()
    size = width, height = 1200, 800+MENUBARHEIGHT+BBARHEIGHT
    pygame.init()
    pygame.display.set_mode(size, RESIZABLE)
    pygame.display.set_caption("RDP Over SMTP")
    setIcon(255,0,0)
    mouse = Mouse()
    mouse.setFunctions(mouseClicked, mouseDragged, mouseMoved, mousePressed, mouseReleased)
    keysDown = dict()
    unicodes = dict()
    badKeys = []
    frameRate = 60
    frameTime = 1/frameRate
    lFrame = 0
    runRate = 1
    runTime = 1/runRate
    lRun = 0
    setIcon(0,255,0)
    postInit()
    while 1:
        dt = abs(time() - lRun)
        dft = abs(time() - lFrame)
        if abs(time() - lRun) > runTime:
            run(dt)
            lRun = time()

        if abs(time() - lFrame) > frameTime:
            mainSurface = draw(pygame.Surface(size), dft)
            pygame.display.get_surface().blit(mainSurface, (0,0))
            lFrame = time()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == VIDEORESIZE:
                width = event.w
                height = event.h
                size = (width, height)
                pygame.display.set_mode((width, height), RESIZABLE)
                if width < 800:
                    width = 800
                    pygame.display.set_mode((width, height), RESIZABLE)
                if height < 600:
                    height = 600
                    pygame.display.set_mode((width, height), RESIZABLE)
            if event.type == MOUSEMOTION:
                mouse.move(event.pos[0], event.pos[1])
            if event.type == MOUSEBUTTONDOWN:
                mouse.mouseDown(event.pos[0], event.pos[1], event.button)
            if event.type == MOUSEBUTTONUP:
                mouse.mouseUp(event.pos[0], event.pos[1], event.button)
            if event.type == KEYDOWN:
                if event.key not in badKeys:
                    if event.key in keysDown.keys():
                        if keysDown[event.key] == 0.0:
                            keysDown[event.key] = time()
                            keyPressed(event.key, event.unicode)
                        else:
                            keyHeld(event.key, event.unicode, time()-keysDown[event.key])
                    else:
                        keysDown[event.key] = time()
                        keyPressed(event.key, event.unicode)
            if event.type == KEYUP:
                if event.key not in badKeys:
                    if keysDown[event.key] != 0:
                        keysDown[event.key] = 0.0
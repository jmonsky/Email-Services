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

# TODO: ADD CROSS PLATFORM MAC/WINDOWS CONTROL / ALT Keys
def keyCombos():
    global SETTINGS
    os = SETTINGS["TargetSystem"]
    return {
            13:"ENTER",
            304:"SHIFT",
            303:"SHIFT",
            306:"CONTROL",
            308:{
                "Windows":"ALT",
                "Linux":"ALT",
                "Mac":"OPTION"
                }[os],
            310:{
                "Windows":"WINDOWS",
                "Linux":"WINDOWS",
                "Mac":"COMMAND"
                }[os],
            311:{
                "Windows":"WINDOWS",
                "Linux":"WINDOWS",
                "Mac":"COMMAND"
                }[os],
            300:"NUM LOCK",
            127:"DELETE",
            277:"INSERT",
            280:"PAGEUP",
            281:"PAGEDOWN",
            278:"HOME",
            279:"END",
            309:{
                "Windows":"WINDOWS",
                "Linux":"WINDOWS",
                "Mac":"COMMAND"
                }[os],
            307:{
                "Windows":"ALT",
                "Linux":"ALT",
                "Mac":"OPTION"
                }[os],
            9:"TAB",
            8:"BACKSPACE",
            27:"ESCAPE",
            282:'F1',
            283:'F2',
            284:'F3',
            285:'F4',
            286:'F5',
            287:'F6',
            288:'F7',
            289:'F8',
            290:'F9',
            291:'F10',
            292:'F11',
            293:'F12',
            301:"CAPSLOCK",
            276:"LEFT",
            273:"UP",
            274:"DOWN",
            275:"RIGHT",
        }

def keyPressed(key, unicode):
    if MENUS[MENU].name == "Remote Control":
        if key in keyCombos().keys():
            unicode = keyCombos()[key]
        global RECORDING, RCSCRIPT, RCTIME
        
        if unicode == "\\":
            unicode = "\\\\\\\\"
        if unicode == " ":
                unicode = "SPACE"
        print(f"Key Pressed {key}, {unicode}")
        if len(unicode) > 0:
            if RECORDING and RCSCRIPT != None:
                if abs(time() - RCTIME) > 0.5 and len(RCSCRIPT.Load()) > 0:
                    RCSCRIPT.addLine(f"`RDP.Sleep {abs(time() - RCTIME)}")
                    RCTIME = time()
                
                RCSCRIPT.addLine(f"`RDP.KeyDown '{unicode}'")


def keyReleased(key):
    global unicodes, RCSCRIPT, RECORDING, RCTIME
    if MENUS[MENU].name == "Remote Control":
        rec = False
        unicode = ""
        if key in unicodes.keys():
            unicode = unicodes[key]
            if unicode == "\\":
                unicode = "\\\\\\\\"
            if unicode == " ":
                unicode = "SPACE"
            rec = True
            print(f"Key Released {key}, {unicode}")
            
        else:
            print(f"Key Released {key}, NO UNICODE")
        if key in keyCombos().keys():
            unicode = keyCombos()[key]
            rec = True
        if rec:
            if len(unicode) > 0:
                    if RECORDING and RCSCRIPT != None:
                        if abs(time() - RCTIME) > 0.5 and len(RCSCRIPT.Load()) > 0:
                            RCSCRIPT.addLine(f"`RDP.Sleep {abs(time() - RCTIME)}")
                            RCTIME = time()
                        RCSCRIPT.addLine(f"`RDP.KeyUp '{unicode}'")

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
            RCSCRIPT.setVariables({})
            MC.sendMail(server_address, f"SERVICE INPUT : {SID} : {ID}", RCSCRIPT.Load())
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
                    if len(RCSCRIPT.lines) > 0 and abs(time() - RCTIME) > 0.5:
                        RCSCRIPT.addLine(f"`RDP.Sleep {abs(time() - RCTIME)}")
                        RCTIME = time()
                    RCSCRIPT.addLine(f"`RDP.ClickAt {(ax / width) * xS} {(ay / (height - MENUBARHEIGHT - BBARHEIGHT)) * yS}")
                elif button == 3:
                    if len(RCSCRIPT.lines) > 0 and abs(time() - RCTIME) > 0.5:
                        RCSCRIPT.addLine(f"`RDP.Sleep {abs(time() - RCTIME)}")
                        RCTIME = time()
                    RCSCRIPT.addLine(f"`RDP.RightClickAt {(ax / width) * xS} {(ay / (height - MENUBARHEIGHT - BBARHEIGHT)) * yS}")

def mouseDragged(drag, button):
    pass

def mouseMoved(x,y,dx,dy, button):
    global BUTTONS, MENUS, MENU
    if y < MENUBARHEIGHT:
        X = 0
        for button in MENUS:
            if x > X and x < button.length + X:
                button.Hover()
            else:
                button.NoHover()
            X = X + button.length + 10
    else:
        for button in MENUS:
            button.NoHover()
    if y > MENUBARHEIGHT and y < MENUBARHEIGHT + BBARHEIGHT:
        X = 0
        for button in BUTTONS[MENU]:
            if x > X and x < button.length + X:
                button.Hover()
            else:
                button.NoHover()
            X = X + button.length + 10
    else:
        for button in BUTTONS[MENU]:
            button.NoHover()
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

def cycleTargetSystem():
    global SETTINGS
    nextSystem = {
        "Windows":"Linux",
        "Linux":"Mac",
        "Mac":"Windows"
    }
    SETTINGS["TargetSystem"] = nextSystem[SETTINGS["TargetSystem"]]

def toggleRev():
    global SETTINGS
    SETTINGS["ReverseMonitor"] = not SETTINGS["ReverseMonitor"]

def upDirectory():
    global VARIABLES

def CycleUpdateTimes():
    global SETTINGS
    SETTINGS["FileUpdateRate"] = SETTINGS["FileUpdateRate"] + 2
    if SETTINGS["FileUpdateRate"] > 20:
        SETTINGS["FileUpdateRate"] = 2

def ToggleUpdates():
    global SETTINGS
    SETTINGS["AutoUpdateFiles"] = not SETTINGS["AutoUpdateFiles"]

def preInit():
    global MENUS, MENU, BUTTONS, BBARHEIGHT, MENUBARHEIGHT, FUNCQ, RECORDING, RCSCRIPT, RCTIME, SETTINGS
    SETTINGS = {
        "Monitor":1,
        "Monitors":1,
        "ReverseMonitor":False,
        "TargetSystem":"Windows",
        "FileUpdateRate":4,
        "AutoUpdateFiles":True,
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
        [
            Button("Quit", function=Exit), 
            Button("Update", function=udpateMail), 
            Button("Screen Shot", function=RequestScreenShot), 
            Button("Start Rec", function=ToggleMacro)
        ], 
        [Button("Quit", function=Exit),], 
        [
            Button("Quit", function=Exit),
            Button("Toggle AutoUpdate", function=ToggleUpdates),
            Button("Upload File"),
            Button("Up Directory", function=upDirectory),
        ],
        [
            Button("Quit", function=Exit),
            Button("Update", function=udpateMail),
            Button("Request Screen Data", function=getScreenData),
            Button("Prev Monitor", function=prevMon),
            Button("Next Monitor", function=nextMon),
            Button("Reverse Monitor", function=toggleRev),
            Button("Cycle System", function=cycleTargetSystem),
            Button("Change Time", function=CycleUpdateTimes),
        ],
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

    global MC, server_address, SC, ID, SID
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
    ID = config["CLIENT_ID"]
    SID = config["SERVER_ID"]
    MC = MailController()
    
    server_address = config["SERVER_ADDRESS"]
    MC.login(username, password,  config["SMTP_ADDRESS"], config["IMAP_ADDRESS"], int(config["SMTP_PORT"]), int(config["IMAP_PORT"]))
    print("Logged In")
    SC = SL.ScriptLoader()

def getScreenData():
    startupScript = SC.getScript("GetScreenData")
    startupScript.setVariables({})
    MC.sendMail(server_address, f"SERVICE INPUT : {SID} : {ID}", startupScript.Load())

def postInit():
    global xS, yS
    global ScreenCaps
    global VARIABLES
    VARIABLES = {
        "Files":[],
        "Dirs":[],
        "Path":"",
        "Listings":[],
    }
    for m in MC.getMail():
        if m.subject.split(":")[0].strip(" ") == "SERVICE OUTPUT" and m.subject.split(":")[1].strip(" ") == ID:
            MC.delMail(m)
    getScreenData()

    ScreenCaps = []

    xS = 1920  
    yS = 1080

def run(dt, runs):
    global ScreenCaps, FUNCQ, MC, SC
    ScreenCaps = [x.update() for x in ScreenCaps]
    for item in FUNCQ:
        if type(item) == Button:
            item.execute()
    FUNCQ = []
    if MENUS[MENU].name == "File Browser" and runs % SETTINGS["FileUpdateRate"] == 0 and SETTINGS["AutoUpdateFiles"]:
        updateScript = SC.getScript("GetFileData")
        updateScript.setVariables({})
        MC.sendMail(server_address, f"SERVICE INPUT : {SID} : {ID}", updateScript.Load())
        udpateMail()

def udpateMail():
    global xS, yS
    global ScreenCaps
    global SETTINGS, VARIABLES
    print(f"Getting Mail {time()}")
    first = False
    for m in MC.getMail():
        if m.subject.split(":")[0].strip(" ") == "SERVICE OUTPUT" and m.subject.split(":")[1].strip(" ") == ID:
            for line in str(m.message).split("\n"):
                if line[:2] == f"%%":
                    args = line.split(" ")
                    print(f"{args[1]}")
                    if "Resolution" in args:
                        xS = int(args[3][:-1])
                        yS = int(args[4])
                    if "Monitors" in args:
                        SETTINGS["Monitors"] = int(args[3])
                    if "Attachment" in args:
                        print("File Found!")
                        filename = StandardDeSerialize(None, line)
                        if filename.split(".")[1].strip("'") == "png":
                            print("Screenshot found")
                            for sc in ScreenCaps:
                                if sc.exists(filename):
                                    break
                            else:
                                ScreenCaps.append(ScreenCap(filename))
                    if "Dir" in args or "File" in args:
                        if not first:
                            first = True
                            VARIABLES["Files"] = []
                            VARIABLES["Dirs"] = []
                    if "Dir" in args:
                        d = " ".join(args[3:])
                        VARIABLES["Dirs"].append(d)
                        VARIABLES["Listings"].append(None)
                    if "File" in args:
                        f = " ".join(args[3:])
                        VARIABLES["Files"].append(f)
                    if "Path" in args:
                        p = " ".join(args[3:])
                        VARIABLES["Path"] = p
            MC.delMail(m)

def RequestScreenShot():
    global SETTINGS
    screenshotScript = SC.getScript("ScreenShot")
    screenshotScript.setVariables(SETTINGS)
    MC.sendMail(server_address, f"SERVICE INPUT : {SID} : {ID}", screenshotScript.Load())
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
    size = width, height = 1280, 720+MENUBARHEIGHT+BBARHEIGHT
    pygame.init()
    pygame.display.set_mode(size, RESIZABLE)
    pygame.display.set_caption("RDP Over SMTP")
    setIcon(255,0,0)
    print("Display Initialized")
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
    runs = 0
    lRun = 0
    setIcon(0,255,0)
    postInit()
    print("Initialized")
    while 1:
        dt = abs(time() - lRun)
        dft = abs(time() - lFrame)
        if abs(time() - lRun) > runTime:
            run(dt, runs)
            runs += 1
            if runs > 1000:
                runs = 0
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
                if len(event.unicode) > 0:
                    unicodes[event.key] = event.unicode
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
                        keyReleased(event.key)
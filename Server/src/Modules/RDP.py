import mss
import pyautogui
import time
pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True

def ScreenShot(vars, monitor=1):
    with mss.mss() as sct:
        return f"'{sct.shot(mon=monitor)}'"

def SS(vars, monitor=1):
    return ScreenShot(monitor)

def PartialScreenShot(vars, x, y, width, height):
    with mss.mss() as sct:
        monitor = {"top": x, "left": y, "width": width, "height": height}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        return output

def PSS(vars, x, y, width, height):
    return PartialScreenShot(vars, x, y, width, height)

def SSAll(vars):
    with mss.mss() as sct:
        return str([filename for filename in sct.save()])

def ClickAt(vars, x, y, t=0):
    pyautogui.click(x, y, duration=t)

def Click(vars, t=0):
    pyautogui.click(duration=t)

def RightClick(vars, t=0):
    pyautogui.rightClick(duration=t)

def RightClickAt(vars, x, y, t=0):
    pyautogui.rightClick(x, y, duration=t)

def MoveMouse(vars,x,y,t=0):
    pyautogui.moveTo(x,y,duration=t)

def MM(vars, x, y, t=0):
    MouseMove(vars, x, y,t)

def MoveRelMouse(vars,dx,dy,t=0):
    pyautogui.moveRel(dx, dy, duration=t)

def MRM(vars, dx, dy, t=0):
    MoveRelMouse(vars, dx, dy, t)

def MouseRelDrag(vars, dx, dy, t=0):
    pyautogui.dragRel(dx, dy, duration=t)

def GetPosition(vars):
    x, y = pyautogui.position()
    return f"'{x}, {y}'"

def Scroll(vars, value):
    pyautogui.scroll(value)

def GetResolution(vars):
    x,y = pyautogui.size()
    return f"'{x}, {y}'"

def Typewrite(vars, key, t=0):
    pyautogui.typewrite(key, interval=t)

def KeyDown(vars, key):
    pyautogui.keyDown(key)

def KeyUp(vars, key):
    pyautogui.keyUp(key)

def Sleep(vars, t):
    time.sleep(t)
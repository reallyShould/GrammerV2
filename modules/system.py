import os
import mss

username = os.getlogin()
scriptPath = os.getcwd()
defaultStartFolder = f'C:\\Users\\{username}\\Desktop'

SYSTEM = {
    "LOCK": "Rundll32.exe user32.dll,LockWorkStation",
    "SHUTDOWN": "shutdown /s /t 00",
    "REBOOT": "shutdown /r /t 00",
    "SLEEP": "rundll32 powrprof.dll,SetSuspendState 0,1,0",
    "LOGOUT": "shutdown /l"
}

def getCurrentDir() -> str:
    return os.getcwd()

def ls(string:list) -> str:
    if len(string) == 1:
        path = getCurrentDir()
    else:
        path = string[1]

    try:
        if path[1] == ":":
            normalizePath = path
        else:
            normalizePath = f"{getCurrentDir()}\\{path}"

        out = f'Folder: `{normalizePath}`\nElements: {len(os.listdir(path))}\n\n'
        files = os.listdir(path)
        for i in files:
            out += f'`{i}`\n==========\n'
        try:
            return out
        except:
            return 'Huge list'
    except:
        return f"Dir not exist: {normalizePath}"

def getScreen() -> str:
    with mss.mss() as sct:
        return sct.shot(mon=-1, output="fullscreen.png")

def mkdir(string:list) -> str:
    try:
        if len(string) != 2:
            return "I need 2 arguments"
        path = string[1]
        if path[1] == ":":
            normalizePath = path
        else:
            normalizePath = f"{getCurrentDir()}\\{path}"
        os.makedirs(normalizePath)
        return f"Done: {normalizePath}"
    except Exception as err:
        return f"{err}"
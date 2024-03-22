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

def normalizeString(string:list) -> str:
    path = string[1]
    if path == "..":
        return path
    if path[1] == ":":
        normalizePath = path
    else:
        normalizePath = f"{getCurrentDir()}\\{path}"
    return normalizePath

def getCurrentDir() -> str:
    return os.getcwd()

def ls(string:list) -> str:
    if len(string) == 1:
        path = getCurrentDir()
    else:
        path = normalizeString(string)
    try:
        out = f'Folder: `{path}`\nElements: {len(os.listdir(path))}\n\n'
        files = os.listdir(path)
        for i in files:
            out += f'`{i}`\n==========\n'
        try:
            return out
        except:
            return 'Huge list'
    except:
        return f"Dir not exist: {path}"

def getScreen() -> str:
    with mss.mss() as sct:
        return sct.shot(mon=-1, output="fullscreen.png")

def mkdir(string:list) -> str:
    try:
        if len(string) != 2:
            return "I need 2 arguments"
        path = normalizeString(string)
        os.makedirs(path)
        return f"Done: {path}"
    except Exception as err:
        return f"{err}"
    
def cd(string:list) -> str:
    try:
        if len(string) != 2:
            return "I need 2 arguments"
        path = normalizeString(string)
        os.chdir(path)
        return ls(["ls"])
    except Exception as err:
        return f"{err}"
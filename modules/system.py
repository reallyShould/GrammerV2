import os

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

def getCurrentDir():
    return os.getcwd()

def ls(path=getCurrentDir()):
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

import os
import mss

import shutil
from distutils.dir_util import copy_tree
from modules.emoj import *

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
        out = f'{FOLDER}Folder: <code>{path}</code>\n{FILE}Elements: {len(os.listdir(path))}\n\n'
        files = os.listdir(path)
        for i in files:
            out += f'<code>{i}</code>\n==========\n'
        try:
            return out
        except:
            return ERROR_STR("Huge list", "WARNING")
    except:
        return ERROR_STR(f"Dir not exist: {path}", "ERROR")

def getScreen() -> str:
    with mss.mss() as sct:
        return sct.shot(mon=-1, output="fullscreen.png")

def mkdir(string:list) -> str:
    try:
        if len(string) != 2:
            return ERROR_STR("I need 1 argument!", "ERROR")
        path = normalizeString(string)
        os.makedirs(path)
        return f"Done: {path}"
    except Exception as err:
        return f"{err}"
    
def cd(string:list) -> str:
    try:
        if len(string) != 2:
            return ERROR_STR("I need 1 argument!", "ERROR")
        path = normalizeString(string)
        os.chdir(path)
        return ls(["ls"])
    except Exception as err:
        return f"{err}"

def copy(string:list) -> str:
    if len(string) != 3:
            return ERROR_STR("I need 2 argument!", "ERROR")
    fromPath = string[1]
    toPath =  string[2]
    try:
        if os.path.isdir(fromPath):
            newFolder = f"{toPath}\\" + fromPath.split('\\')[-1]
            os.mkdir(newFolder)
            copy_tree(fromPath, newFolder)
            
            return f"{DONE}Copy {fromPath} to {toPath}"
        else:
            shutil.copy(fromPath, toPath)
            return f"{DONE}Copy {fromPath} to {toPath}"
    except Exception as err:
        if err is FileExistsError:
            return ERROR_STR(f"File \"{fromPath}\" not exist", "ERROR")
        return ERROR_STR(f"Something wrong: {err}", "ERROR")
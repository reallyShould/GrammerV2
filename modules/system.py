import os
import mss
import subprocess
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
        return "\\".join(getCurrentDir().split("\\")[:-1:])
    elif path == ".":
        return getCurrentDir()
    elif path == "~":
        return f"C:\\Users\\{username}"
    if ":" in path:
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
        return ERROR_STR(f"Something wrong: {err}", "ERROR")
    
def cd(string:list) -> str:
    try:
        if len(string) != 2:
            return ERROR_STR("I need 1 argument!", "ERROR")
        path = normalizeString(string)
        os.chdir(path)
        return ls(["ls"])
    except Exception as err:
        return ERROR_STR(f"Directory \"{path}\" not exist", "ERROR")

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
    
def remove(string:list) -> str:
    if len(string) != 2:
        return ERROR_STR("I need 1 argument!", "ERROR")
    path = string[1]
    try:
        if os.path.isdir(path) == True:
            rnpath = os.getcwd()
            os.chdir(path)
            filesForDel = os.listdir()
            for i in filesForDel:
                remove(["rm", i])
            os.chdir(rnpath)
            os.rmdir(path)
            return f"{DONE}\"{path}\" has been deleted."
        else:
            os.remove(path)
            return f"{DONE}\"{path}\" has been deleted."
    except Exception as err:
        return ERROR_STR(f"Something wrong: {err}", "ERROR")

def move(string:list) -> str:
    if len(string) != 3:
        return ERROR_STR("I need 2 argument!", "ERROR")
    fromPath = string[1]
    toPath =  string[2]
    try:
        if os.path.isdir(fromPath):
            newFolder = f"{toPath}\\" + fromPath.split('\\')[-1]
            os.mkdir(newFolder)
            copy_tree(fromPath, newFolder)
            remove(["", fromPath])
            return f"{DONE}Copy {fromPath} to {toPath}"
        else:
            shutil.copy(fromPath, toPath)
            os.remove(fromPath)
            return f"{DONE}Move {fromPath} to {toPath}"
    except Exception as err:
        if err is FileExistsError:
            return ERROR_STR(f"File \"{fromPath}\" not exist", "ERROR")
        return ERROR_STR(f"Something wrong: {err}", "ERROR")

def start(string:list) -> str:
    if len(string) == 1:
        return ERROR_STR("I need argument!", "ERROR")
    success = 0
    files = string[1::]
    filesLen = len(files)
    for i in range(filesLen):
        if not os.system(f"start {files[i]}"):
            success += 1
    if success != filesLen:
        return ERROR_STR(f"Not all files were opened. ({success}/{filesLen})", "WARNING")
    else:
        return f"{DONE}All files were opened. ({success}/{filesLen})"

def cmdNoStd(string:list) -> str:
    command = " ".join(string[1::])
    if len(string) == 1:
        return ERROR_STR("I need argument!", "ERROR")
    if not os.system(command):
        return f"{DONE}The command executed without errors."
    else: 
        return ERROR_STR(f"Command not recognized: \"{command}\"", "ERROR")

def cmdStd(string:list) -> str:
    if len(string) == 1:
        return ERROR_STR("I need argument!", "ERROR")
    command = string[1::]
    try:
        return subprocess.check_output(command)
    except:
        return ERROR_STR(f"Command not recognized!", "ERROR")

def cat(string:list) -> str:
    try:
        if len(string) != 2:
            return ERROR_STR("I need 1 argument!", "ERROR")
        path = normalizeString(string)
        with open(path, "r") as f:
            text = f.read()
            if text.strip() == "":
                return ERROR_STR(f"File is empty!", "WARNING")
            elif len(text) > 4000:
                return ERROR_STR(f"File too large", "WARNING")
            return f"<code>{text}</code>"
    except Exception as err:
        return ERROR_STR(f"Something wrong: {err}", "ERROR")

def touch(string:list) -> str:
    try:
        if len(string) != 2:
            return ERROR_STR("I need 1 argument!", "ERROR")
        path = normalizeString(string)
        if os.path.exists(path):
            return ERROR_STR(f"File already exist!", "WARNING")
        with open(path, "a+") as f:
            pass
        return f"{DONE}File {path} created."
    except Exception as err:
        return ERROR_STR(f"Something wrong: {err}", "ERROR")
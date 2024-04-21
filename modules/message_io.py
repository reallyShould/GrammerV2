import os

from modules.emoj import *
import modules.system as system

def splitter(text):
    text = text.replace("\\ ", "\\s")
    tmp = text.strip().split(" ")

    out = []
    for i in tmp:
        i = i.replace("\\s", " ")
        out.append(i)
    return out

def messageProcessing(message:str):
    if message in system.SYSTEM.keys():
        os.system(system.SYSTEM[message])
        return f"Trying system: {message}"
    
    mes = splitter(message)
    command = mes[0]
    
    #basic
    if command == "ls":
        return system.ls(mes)
    elif command == "mkdir":
        return system.mkdir(mes)
    elif command == "cd":
        return system.cd(mes)
    elif command == "cp":
        return system.copy(mes)
    elif command == "mv":
        return system.move(mes)
    elif command == "rm":
        return system.remove(mes)
    elif command == "start":
        return system.start(mes)
    elif command == "getfile":
        return system.getfile(mes)
    elif command == "cmd":
        return system.cmdNoStd(mes)
    elif command == "cmd2":
        return system.cmdStd(mes)
    elif command == "cat":
        return system.cat(mes)
    elif command == "touch":
        return system.touch(mes)
    else:
        return f"{QUESTION}Your command is not recognized"
    

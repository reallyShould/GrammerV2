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
        pass
    elif command == "rm":
        pass
    elif command == "start":
        pass
    elif command == "getfile":
        pass
    elif command == "cmd":
        pass
    elif command == "cmd2":
        pass
    elif command == "cat":
        pass
    elif command == "touch":
        pass
    else:
        return f"{QUESTION}Your command is not recognized"
    

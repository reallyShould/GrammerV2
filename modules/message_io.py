import os

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
        pass
    elif command == "cd":
        pass
    elif command == "cp":
        pass
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
        return "???"
    
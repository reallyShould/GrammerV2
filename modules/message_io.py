import os

import modules.system as system

def splitter(text):
    text = text.replace('  ', ' ')
    tmp = text.strip().split(' ')

    out = []
    for i in tmp:
        i = i.replace('\\s', ' ')
        out.append(i)
    return out

def messageProcessing(message:str):
    if message in system.SYSTEM.keys():
        os.system(system.SYSTEM[message])
        return f"Trying system: {message}"
    
    mes = splitter(message)
    command = mes[0]
    print(mes)
    print(command)

    if command == 'ls':
        if len(mes) == 1:
            return system.ls()
        else:
            return system.ls(mes[1])
    else:
        return "???"
    

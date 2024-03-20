import telebot

import modules.file_io as file_io
import modules.message_io as mes_io

TOKEN_PATH = "token.txt"
START = "data/message.txt"

bot = telebot.TeleBot(file_io.readFile(TOKEN_PATH))

@bot.message_handler(commands=["start", "info", "help"])

def start_message(message):
    bot.send_message(message.chat.id, file_io.readFile(START), parse_mode="Markdown")

@bot.message_handler(content_types=["text"])

def text(message):
    bot.send_message(message.chat.id, mes_io.messageProcessing(message.text), parse_mode="Markdown")

bot.polling(non_stop=True)
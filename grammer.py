import telebot

import modules.file_io as file_io

TOKEN_PATH = "token.txt"

bot = telebot.TeleBot(file_io.readFile(TOKEN_PATH))

@bot.message_handler(commands=["start", "info", "help"])

def start_message(message):
    bot.send_message(message.chat.id, "Start is done")

bot.polling(non_stop=True)
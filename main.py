import telebot
from telebot.types import Message
from units import *


bot = telebot.TeleBot(return_bot_token())



@bot.message_handler(commands=['start'])
def start_bot(message: Message):
    bot.send_message(message.from_user.id, f"Приветсвую тебя, {message.from_user.username}!\n"
                                           f"Я первый в мире бот астротаролог, смогу...") #17.07.24 21:21 - я плачу

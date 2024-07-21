import datetime
import telebot
from telebot.types import Message, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from utils import *
from sql_database import *
from configs import *
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename='logs.txt',
    filemode="a"
)

bot = telebot.TeleBot(get_bot_token())

create_databases()
logging.info("Базы данных успешно подключены")


def create_reply_keyboard(buttons_list: list) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard


def create_inline_keyboard(buttons_dict: dict) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for button_text, callback_data in buttons_dict.items():
        button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
        keyboard.add(button)
    return keyboard


@bot.message_handler(commands=['start'])
def start_bot(message: Message):
    bot.send_message(message.from_user.id,
                     f"Тут должно быть привественное сообщение, но его не будет, потому что мне не заплатили.")
    if not check_user_exists(message.from_user.id):
        add_user(message.from_user.id,
                 [message.from_user.username, None, datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'), None])
    ...

@bot.message_handler(commands=['help'])
def send_help(message: Message):
    bot.send_message(message.from_user.id,
                     'Тут должно быть сообщение для помощи, но к сожалению его нет. Используйте команду /add_question чтобы задать вопрос специалисту.')
    logging.info(f'{message.from_user.username} обратился за помощью')


@bot.message_handler(commands=['add_question'])
def add_new_question(message: Message):
    bot.send_message(message.from_user.id, "Напишите свой вопрос на который должен ответить специалист:")
    bot.register_next_step_handler(message, help_user)
    ...

def help_user(message: Message):
    ...

@bot.message_handler(commands=['admin_help_user'])
def send_admin_help(message: Message):
    """Команда администраторов"""
    ...

@bot.callback_query_handler(func=lambda call: True)
def callback_help(call):
    ...


if __name__ == '__main__':
    bot.polling()
    logging.info('Бот запущен успешно')

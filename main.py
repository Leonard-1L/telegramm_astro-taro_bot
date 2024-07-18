import telebot
from telebot.types import Message, KeyboardButton, ReplyKeyboardMarkup
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


@bot.message_handler(commands=['start'])
def start_bot(message: Message):
    bot.send_message(message.from_user.id,
                     f"Напиши приветсвие для бота, его краткое описание. В общем то, что хочешь видеть когда твой бот отвечает после команды /start.")
    add_message(message.from_user.id, ['message.from_user.username', None])


@bot.message_handler(commands=['help'])
def send_help(message: Message):
    logging.info(f'{message.from_user.username} обратился за помощью')
    bot.send_message(message.from_user.id,
                     'Тут должно быть сообщение для помощи. Напишите чем вам нужно помочь, вам ответят в течение суток.')
    bot.register_next_step_handler(message, help_user)


def help _user(message: Message):
    for admin in admins_id:
        bot.send_message(admin, f"{message.from_user.username} попросил помощь: '{message.text}'",
                         reply_markup=create_keyboard(['Я отвечу', "Не смогу ответить"]))



@bot.message_handler(commands=['ADMINS_send_help'])
def send_admins_help(message: Message):


def create_keyboard(buttons_list: list) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard


if __name__ == '__main__':
    create_database()
    logging.info("База данных успешно создана")
    bot.polling()
    logging.info('Бот запущен успешно')

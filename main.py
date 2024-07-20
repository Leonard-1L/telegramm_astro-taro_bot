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
logging.info("Базы данных успешно созданы")


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
                     f"Мам, напиши мне приветсвие для бота, его краткое описание. В общем то, что хочешь видеть когда твой бот отвечает после команды /start.")
    if not check_user_exists(message.from_user.id):
        add_user(message.from_user.id,
                 [message.from_user.username, None, datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'), None])


@bot.message_handler(commands=['help'])
def send_help(message: Message):
    logging.info(f'{message.from_user.username} обратился за помощью')
    bot.send_message(message.from_user.id,
                     'Тут должно быть сообщение для помощи. Напишите чем вам нужно помочь, вам ответят в течение суток.')
    bot.register_next_step_handler(message, help_user)


def help_user(message: Message):
    add_question(message.from_user.id, [message.text, 'Не решён', None])
    bot.reply_to(message, 'Помощник в пути!')
    for admin in admins_id:
        bot.send_message(admin,
                         f"{message.from_user.username} попросил помощь: '{message.text}'\n Используй команду /admin_help_user чтобы помочь.")
    return


@bot.message_handler(commands=['admin_help_user'])
def send_admin_help(message: Message):
    """Команда администраторов"""
    if message.from_user.id not in admins_id:
        bot.send_message(message.from_user.id,
                         "Извините, но у вас нет доступа к командам администраторов. Если нужна помощь, используйте /help.")
        return
    questions = return_all_questions()
    for question in questions:
        if question[3] == 'Не решён':
            keyboard = create_inline_keyboard({"Я отвечу!": question[0]})
            bot.send_message(message.from_user.id, f'Вопрос от {question[1]}: {question[2]}', reply_markup=keyboard)
        elif question[3] == 'Решается' and question[4] == message.from_user.id:
            bot.send_message(message.from_user.id,
                             f"Помоги пользователю: {question[2]}\nОтвет пиши сразу, единым сообщением.")
            bot.register_next_step_handler(message, send_admins_help)


def send_admins_help(message: Message):
    questions = return_all_questions()
    for question in questions:
        if question[3] == 'Решается' and message.from_user.id == question[4]:
            question_id, user_id, user_question, status, responding_admin = question
            if user_id:
                update_value('questions', 'status', 'status', user_id=user_id, individual_value='Решается',
                             new_column_value="Решён")
                bot.send_message(user_id, message.text)
            else:
                logging.error('Какая-то фигня, пользователь, который запросил помощь, не найден.')
            return


@bot.callback_query_handler(func=lambda call: True)
def callback_help(call):
    question_id, user_id, user_question, status, responding_admin = return_question_by_id(call.data)
    if status == "Решается":
        bot.send_message(call.from_user.id, "Вопрос уже решается другим специалистом, отлично!")
        return

    elif status == "Решён":
        bot.send_message(call.from_user.id, "Другой специалист уже решил вопрос, отлично!")
        return

    update_value('questions',
                 'status',
                 'question_id',
                 user_id=user_id,
                 individual_value=question_id,
                 new_column_value='Решается')

    update_value('questions',
                 'responding_admin',
                 'question_id',
                 user_id=user_id,
                 individual_value=question_id,
                 new_column_value=call.from_user.id)

    admins_id.remove(call.from_user.id)
    try:
        for admin in admins_id:
            bot.send_message(admin, f'{call.from_user.id} начал отвечать на "{user_question}"')
    except Exception as e:
        print(e)

    bot.send_message(call.from_user.id, "Напиши ответ для помощи пользователю.\nОтвет пиши сразу, единым сообщением.")
    logging.info(f'{call.from_user.username} начал отвечать на вопрос с id {question_id}')
    bot.register_next_step_handler_by_chat_id(call.from_user.id, send_admins_help)


if __name__ == '__main__':
    bot.polling()
    logging.info('Бот запущен успешно')

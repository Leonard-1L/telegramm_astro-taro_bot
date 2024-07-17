import sqlite3

import sqlite3
import logging
from config import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=LOGS,
    filemode="w"
)

path_to_db = 'user.db'


def create_database():
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                user_name TEXT,
                user_city TEXT)
            ''')
            logging.info("DATABASE: База данных создана")
    except Exception as e:
        logging.error(f"ошибка при создании таблицы: {e}")
        return None


def add_message(user_id, full_message):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            message, role, total_gpt_tokens, tts_symbols, stt_blocks = full_message
            cursor.execute('''
                    INSERT INTO messages (user_id, message, role, total_gpt_tokens, tts_symbols, stt_blocks) 
                    VALUES (?, ?, ?, ?, ?, ?)''',
                           (user_id, message, role, total_gpt_tokens, tts_symbols, stt_blocks)
                           )
            conn.commit()
            logging.info(f"DATABASE: INSERT INTO messages "
                         f"VALUES ({user_id}, {message}, {role}, {total_gpt_tokens}, {tts_symbols}, {stt_blocks})")
    except Exception as e:
        logging.error(e)
        return None


def select_n_last_messages(user_id, n_last_messages=COUNT_LAST_MSG):
    messages = []
    total_spent_tokens = 0
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT message, role, total_gpt_tokens FROM messages WHERE user_id=? ORDER BY id DESC LIMIT ?''',
                           (user_id, n_last_messages))
            data = cursor.fetchall()
            if data and data[0]:
                for message in reversed(data):
                    messages.append({'text': message[0], 'role': message[1]})
                    total_spent_tokens = max(total_spent_tokens,
                                             message[2])
            return messages, total_spent_tokens
    except Exception as e:
        logging.error(e)
        return messages, total_spent_tokens


def count_all_limits(user_id, limit_type):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''SELECT SUM({limit_type}) FROM messages WHERE user_id=?''', (user_id,))
            data = cursor.fetchone()
            if data and data[0]:
                logging.info(f"DATABASE: У user_id={user_id} использовано {data[0]} {limit_type}")
                return data[0]
            else:
                return 0
    except Exception as e:
        logging.error(e)
        return 0


def count_all_tokens():
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''SELECT SUM(total_gpt_tokens) FROM messages''', )
            data = cursor.fetchone()
            if data and data[0]:
                logging.info(f"DATABASE: Всего затрачено {data[0]}")
                return data[0]
            else:
                return 0
    except Exception as e:
        logging.error(e)
        return 0


def count_users(user_id):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT COUNT(DISTINCT user_id) FROM messages WHERE user_id <> ?''', (user_id,))
            count = cursor.fetchone()[0]
            return count
    except Exception as e:
        logging.error(e)
        return None

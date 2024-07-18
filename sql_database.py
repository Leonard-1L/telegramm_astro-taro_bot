import sqlite3
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename='logs.txt',
    filemode="a"
)

path_to_db = 'users.db'


def create_database():
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                user_name TEXT,
                user_city TEXT)
            ''')
            logging.info("DATABASE: База данных создана")
    except Exception as e:
        logging.error(f"ошибка при создании таблицы: {e}")
        return None


def add_message(user_id, full_message: list):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            user_name, user_city = full_message
            cursor.execute('''
                    INSERT INTO users (user_id, user_name, user_city) 
                    VALUES (?, ?, ?)''',
                           (user_id, user_name, user_city)
                           )
            conn.commit()
            logging.info(f"DATABASE: INSERT INTO users "
                         f"VALUES ({user_id}, {user_name}, {user_city})")
    except Exception as e:
        logging.error(e)
        return None


def count_users(user_id):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT COUNT(DISTINCT user_id) FROM users WHERE user_id <> ?''', (user_id,))
            count = cursor.fetchone()[0]
            return count
    except Exception as e:
        logging.error(e)
        return None


def update_value(column_name, user_id, old_value, new_value):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            query = f"""
                UPDATE users
                SET {column_name} = ?
                WHERE {column_name} = ? AND user_id = ?;
                """
            cursor.execute(query, (new_value, old_value, user_id))
            conn.commit()
        logging.info(f"{user_id} изменил в {column_name} старое значение {old_value} на новое {new_value}")
    except Exception as e:
        logging.error(e)
        return None


def return_value_from_cell(column_name, user_id):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            query = f"""
                SELECT {column_name} FROM users WHERE user_id = ?
                """
            cursor.execute(query, (user_id,))
            conn.commit()
    except Exception as e:
        logging.error(e)
        return None

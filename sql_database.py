import sqlite3
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename='logs.txt',
    filemode="a"
)

path_to_db = 'sqlite.db'


def create_databases():
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                user_name TEXT,
                user_city TEXT,
                registration_date DATETIME,
                date_of_birth DATA)
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                question_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                user_question TEXT,
                status TEXT,
                responding_admin TEXT)
            ''')
            conn.commit()
    except Exception as e:
        logging.error(f"ошибка при создании таблицы: {e}")
        return None


def add_user(user_id, full_message: list):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            user_name, user_city, registration_date, date_of_birth = full_message
            cursor.execute('''
                    INSERT INTO users (user_id, user_name, user_city, registration_date, date_of_birth) 
                    VALUES (?, ?, ?, ?, ?)''',
                           (user_id, user_name, user_city, registration_date, date_of_birth)
                           )
            conn.commit()
            logging.info(
                f"DATABASE: Добавлены значения {user_id}, {user_name}, {user_city}, {registration_date}, {date_of_birth}")
    except Exception as e:
        logging.error(f'add_user: {e}')
        return None


def check_user_exists(user_id):
    with sqlite3.connect(path_to_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        user = cursor.fetchone()
        return True if user else False


def add_question(user_id, full_message: list):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            user_question, status, responding_admin = full_message
            cursor.execute(f'''
                    INSERT INTO questions (user_id, user_question, status, responding_admin)
                    VALUES (?, ?, ?, ?)''',
                           (user_id, user_question, status, responding_admin)
                           )
            conn.commit()
            logging.info(f"DATABASE: Добавлены значения {user_id}, {user_question}, {status}, {responding_admin}")
    except Exception as e:
        logging.error(f'add_question: {e}')


def update_value(table, column_name, individual_column, user_id, individual_value, new_column_value):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            query = f"""
                UPDATE {table}
                SET {column_name} = ?
                WHERE {individual_column} = ? AND user_id = ?;
                """
            cursor.execute(query, (new_column_value, individual_value, user_id))
            conn.commit()
        logging.info(
            f"DATABASE:{user_id} изменил в {column_name} старое значение '{individual_value}' на новое '{new_column_value}'")
    except Exception as e:
        logging.error(f'update_value: {e}')
        return None


def return_value_from_users(column_name, user_id):
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            query = f"""
                SELECT {column_name} FROM users WHERE user_id = ?
                """
            cursor.execute(query, (user_id,))
            conn.commit()
    except Exception as e:
        logging.error(f'return_value_from_users: {e}')
        return None


def return_all_questions() -> list:
    try:
        messages = []
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT question_id, user_id, user_question, status, responding_admin FROM questions")
            rows = cursor.fetchall()
            for row in rows:
                question_id, user_id, user_question, status, responding_admin = row
                message = [question_id, user_id, user_question, status, responding_admin]
                messages.append(message)
            return messages
    except Exception as e:
        logging.error(f'return_all_questions: {e}')


def return_question_by_id(question_id) -> list:
    try:
        with sqlite3.connect(path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT question_id, user_id, user_question, status, responding_admin FROM questions WHERE question_id = ?",
                (question_id,))
            row = cursor.fetchone()
            return row
    except Exception as e:
        logging.error(f'return_question_by_id: {e}')

# def return_question(question_id=None, user_id=None):
#     if not (question_id or user_id):
#         logging.info("Не указаны ни question_id, ни user_id")
#         return []
#
#     messages = []
#     try:
#         with sqlite3.connect(path_to_db) as conn:
#             cursor = conn.cursor()
#             query = "SELECT question_id, user_id, user_question, status, responding_admin FROM questions"
#             params = {}
#             if question_id:
#                 query += " AND question_id = ?"
#                 params['question_id'] = question_id
#             if user_id:
#                 query += " OR user_id = ?"
#                 params['user_id'] = user_id
#             cursor.execute(query, params)
#             rows = cursor.fetchall()
#             for row in rows:
#                 question_id, user_id, user_question, status, responding_admin = row
#                 message = {
#                     'question_id': question_id,
#                     'user_id': user_id,
#                     'user_question': user_question,
#                     'status': status,
#                     'responding_admin': responding_admin
#                 }
#                 messages.append(message)
#             return messages
#     except Exception as e:
#         logging.error(f"Ошибка при работе с базой данных: {e}")
#         raise

import psycopg2
import datetime

conn = None
cur = None

conn = psycopg2.connect(
host="localhost",
port=5432,
database="tg",
user="admin",
password="admin")
cur = conn.cursor()

class Orders:
    def __init__(self, username, sum, course_thb, course_rub, marje, gain, completed, review, rating):
        self.username = username
        self.sum = sum
        self.course_thb = course_thb
        self.course_rub = course_rub
        self.marje = marje
        self.gain = gain
        self.completed = completed
        self.review = review
        self.rating = rating
    
def check_user_exists(chat_id) -> bool:
    'Проверяем наличие пользователя в бд r: true/false'
    cur.execute("SELECT * FROM users WHERE chat_id = '%s'", (chat_id,))
    result = cur.fetchone()
    if result:
        return True
    else:
        return False

def add_new_user(chat_id, name) -> None:
    'Добавляем пользователя в бд'
    cur.execute("INSERT INTO users (name, chat_id) VALUES (%s, %s)", (name, chat_id))
    conn.commit()

def get_chat_id(name: str) -> str:
    'Поиск пользователя по имени'
    name_clean =  name.replace("@", "").strip()
    cur.execute("SELECT chat_id FROM users WHERE name = %s", (name_clean,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None
    
def find_name(chat_id) -> str:
    'Поиск имени пользователя по chat_id'
    cur.execute("SELECT name FROM users WHERE chat_id = '%s'", (chat_id,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None
    
def request_on(chat_id) -> None:
    cur.execute("UPDATE users SET request = TRUE WHERE chat_id = '%s'", (chat_id,))
    conn.commit()

def check_request(chat_id) -> bool:
    'Проверяем наличие запроса в бд r: true/false'
    cur.execute("SELECT request FROM users WHERE chat_id = %s", (chat_id,))
    result = cur.fetchone()
    if result[0] == 1:
        return True
    else:
        return False

def change_logo_text(text):
    cur.execute("UPDATE state_data SET  text = %s WHERE type='logo'", (text,))
    conn.commit()

def get_logo_text():
    'Получаем приветсвенный текст из БД'
    cur.execute("SELECT text FROM state_data WHERE type='logo'")
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None
    
def get_info_text():
    'Получаем приветсвенный текст из БД'
    cur.execute("SELECT text FROM state_data WHERE type='info'")
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None
    
def get_review_link():
    'Получаем строку из бд ("Summer_Death")'
    cur.execute("SELECT text FROM state_data WHERE type='review_link'")
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None
    
def get_banks(language: str):
    '''
    language: 'rus' or 'eng'
    Получаем строку банков из таблицы banks [""]
    '''
    cur.execute(f"SELECT {language} FROM banks")
    result = cur.fetchall()
    cleaned_result = [row[0].strip() for row in result]
    return cleaned_result


def get_trade_methods():
    '''Получаем ключ значени из таблицы banks
    'Себрбанк': 'Sberbank'
    '''
    cur.execute("Select * from banks")
    result = cur.fetchall()
    tm={}
    for row in result:
        key = row[1].strip()  # Предположим, что первый столбец - ключ
        value = row[2].strip()  # Предположим, что второй столбец - значение

        tm[key] = value
    return tm

def create_order(ids, username, user_pay, admin_pay, course_thb, course_rub, marje, gain, tradeMethod, user_bat, user_usdt):
    set = f"INSERT INTO orders (ids, username, user_pay, admin_pay, course_thb, course_rub, marje, gain, trade_method, completed, date, user_bat, user_usdt) VALUES ('{ids}', '{username}', {user_pay}, {admin_pay}, {course_thb}, {course_rub}, {marje}, {gain}, '{tradeMethod}', 'request', '{datetime.datetime.now()}', {user_bat}, {user_usdt})"
    print(set)
    cur.execute(set)
    conn.commit()

def check_order_id(id:str):
    cur.execute("SELECT ids FROM orders WHERE ids = %s", (id,))
    result = cur.fetchone()
    if result:
        return True
    else:
        return False
    

def set_progress(ids: str):
    cur.execute("UPDATE orders SET completed = 'progress' WHERE ids = %s", (ids,))
    conn.commit()

def set_complete(ids: str):
    cur.execute("UPDATE orders SET completed = 'complete' WHERE ids = %s", (ids,))
    conn.commit()

def set_mark(ids: str, mark):
    cur.execute(f"UPDATE orders SET mark = {mark} WHERE ids = '{ids}'",)
    conn.commit()

def set_review(ids:str, rev: str) -> None:
    cur.execute(f"UPDATE orders SET review = '{rev}' WHERE ids = '{ids}'",)
    conn.commit()

def get_orders_in_progress():
    cur.execute("SELECT * FROM orders WHERE completed = 'progress'")
    result = cur.fetchall()
    return result

def get_orders_complete():
    cur.execute("SELECT * FROM orders WHERE completed = 'complete'")
    result = cur.fetchall()
    return result

def get_orders_request():
    cur.execute("SELECT * FROM orders WHERE completed = 'request'")
    result = cur.fetchall()
    return result


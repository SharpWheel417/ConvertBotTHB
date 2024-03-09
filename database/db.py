from datetime import datetime
from database.connect import cur, conn

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
    q = "SELECT * FROM users WHERE chat_id = '%s'"
    cur.execute(q, (chat_id,))
    result = cur.fetchone()
    return bool(result)

def add_new_user(chat_id, name, first_name) -> None:
    'Добавляем пользователя в бд'
    # Проверяем, существует ли пользователь с указанным chat_id
    print(f"Проверяем, существет ли пользователь {chat_id}")
    if name is None:
        name = "--"+first_name
    if first_name is None:
        name = '--unknow_user'
    cur.execute("SELECT id FROM users WHERE chat_id = '%s'", (chat_id,))
    existing_user = cur.fetchone()

    # Если пользователь существует, не выполняем вставку
    if existing_user:
        print("Пользователь с таким chat_id уже существует")
    else:
        # Вставляем пользователя, если он не существует
        print("Новый пользователь добавлен")
        cur.execute("INSERT INTO users (name, chat_id) VALUES (%s, %s)", (name, chat_id))
        conn.commit()  # Не забудьте подтвердить транзакцию, если требуется


def get_chat_id(name: str) -> str:
    'Поиск пользователя по имени'
    name_clean =  name.replace("@", "").strip()
    cur.execute("SELECT chat_id FROM users WHERE name = %s", (name_clean,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None
    
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

def create_order(ids, username, chat_id, user_bat, user_rub, user_usdt, marje, gain_rub, gain_usdt, trade_method):
    date = datetime.now()
    set = f"INSERT INTO orders (ids, username, chat_id, user_bat, user_rub, user_usdt, marje, gain_rub, gain_usdt, trade_method, completed, date) VALUES ('{ids}', '{username}', '{chat_id}', {user_bat}, {user_rub}, {user_usdt}, {marje}, {gain_rub}, {gain_usdt}, '{trade_method}', 'progress', '{date}')"
    print(set)
    cur.execute(set)
    conn.commit()

def update_order(ids, completed):
    update_query = "UPDATE orders SET completed = %s WHERE ids = %s"
    cur.execute(update_query, (completed, ids))
    conn.commit()

def check_order_id(id:str):
    cur.execute("SELECT ids FROM orders WHERE ids = %s", (id,))
    result = cur.fetchone()
    if result:
        return True
    else:
        return False


def set_mark(ids: str, mark):
    cur.execute(f"UPDATE orders SET mark = {mark} WHERE ids = '{ids}'",)
    conn.commit()

def set_review(ids:str, rev: str) -> None:
    cur.execute(f"UPDATE orders SET review = '{rev}' WHERE ids = '{ids}'",)
    conn.commit()

def get_orders_in_progress():
    cur.execute("SELECT * FROM orders WHERE completed = 'in progress'")
    result = cur.fetchall()
    return result

def get_orders_complete():
    cur.execute("SELECT * FROM orders WHERE completed = 'completed'")
    result = cur.fetchall()
    return result

def get_orders_request():
    cur.execute("SELECT * FROM orders WHERE completed = 'progress'")
    result = cur.fetchall()
    return result

def get_orders_cancle():
    cur.execute("SELECT * FROM orders WHERE completed = 'cancle'")
    result = cur.fetchall()
    return result

def get_ready():
    cur.execute("SELECT count(*) FROM orders WHERE completed = 'completed'")
    count = cur.fetchone()[0]
    return count

def get_revenue():
    cur.execute("SELECT sum(gain_rub) FROM orders WHERE completed = 'completed'")
    result = cur.fetchone()[0]
    return round(float(result),2)

def get_marks():
    cur.execute("SELECT avg(mark) FROM orders WHERE completed = 'completed'")
    result = cur.fetchone()[0]
    if result:
        return round(float(result),2)
    else:
        return 0

def get_users():
    cur.execute("SELECT * FROM users")
    return cur.fetchall()

def set_bats(chat_id, bats):
    q = f"INSERT INTO user_state (bat, chat_id) VALUES ({bats}, '{chat_id}') ON CONFLICT (chat_id) DO UPDATE SET bat = {bats}"
    print(q)
    cur.execute(q)
    conn.commit()

def get_bats(chat_id):
    cur.execute(f"SELECT bat FROM user_state WHERE chat_id = '{chat_id}'")
    result = cur.fetchone()
    if result:
        return float(result[0])
    else:
        return None
import psycopg2

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

def find_chat_id(name: str) -> str:
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

def create_order(username, user_pay, admin_pay, course_thb, course_rub, marje, gain):
    cur.execute(f"INSERT INTO orders (username, user_pay, admin_pay, course_thb, course_rub, marje, gain) VALUES ('{username}', {user_pay}, {admin_pay}, {course_thb}, {course_rub}, {marje}, {gain})")
    conn.commit()




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
    
def check_user_exists(chat_id):
    cur.execute("SELECT * FROM users WHERE chat_id = '%s'", (chat_id,))
    result = cur.fetchone()
    if result:
        return True
    else:
        return False

def add_new_user(chat_id, name):
    cur.execute("INSERT INTO users (name, chat_id) VALUES (%s, %s)", (name, chat_id))
    conn.commit()

def find_chat_id(name: str):
    name_clean =  name.replace("@", "").strip()
    cur.execute("SELECT chat_id FROM users WHERE name = %s", (name_clean,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None
    
def find_name(chat_id):
    cur.execute("SELECT name FROM users WHERE chat_id = '%s'", (chat_id,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None
    
def request_on(chat_id):
    cur.execute("UPDATE users SET request = TRUE WHERE chat_id = '%s'", (chat_id,))
    conn.commit()

def check_request(chat_id):
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
    cur.execute("SELECT text FROM state_data WHERE type='logo'")
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return None
    
def get_banks(language: str):
    cur.execute(f"SELECT {language} FROM banks")
    result = cur.fetchall()
    return result
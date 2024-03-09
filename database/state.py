from database.connect import cur, conn

def get_state(chat_id):
    cur.execute(f"SELECT state FROM user_state WHERE chat_id = '{chat_id}'")
    result = cur.fetchone()
    if result:
        return result[0].replace(" ","")
    else:
        return None

def set_state(chat_id, state):
    q = f"INSERT INTO user_state (state, chat_id) VALUES ('{state}', '{chat_id}') ON CONFLICT (chat_id) DO UPDATE SET state = '{state}'"
    print(q)
    cur.execute(q)
    conn.commit()


def set_state_calc(chat_id, calculate):
    q = f"INSERT INTO user_state (calculate, chat_id) VALUES ('{calculate}', '{chat_id}') ON CONFLICT (chat_id) DO UPDATE SET calculate = '{calculate}'"
    print(q)
    cur.execute(q)
    conn.commit()

def get_state_calc(chat_id):
    cur.execute(f"SELECT calculate FROM user_state WHERE chat_id = '{chat_id}'")
    result = cur.fetchone()
    if result:
        return result[0].replace(" ","")
    else:
        return None


def get_order(chat_id):
    cur.execute(f"SELECT order FROM users WHERE chat_id = '{chat_id}'")
    result = cur.fetchone()
    if result:
        return result[0].replace(" ","")
    else:
        return None
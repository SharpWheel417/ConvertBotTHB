from database.connect import cur

def get_mess(type: str, admin: bool) -> str:
    q = "SELECT text FROM state_data WHERE type = %s AND admin = %s"
    cur.execute(q, (type, admin))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        return "No message found for the given type"
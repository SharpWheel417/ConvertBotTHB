from connect import cur


def get_mess(type:str) -> str:

    return cur.execute("SELECT text FROM state_data WHERE type = %s", (type,)).fetchone()[0]

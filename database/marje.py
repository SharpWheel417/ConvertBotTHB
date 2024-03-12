import psycopg2
from database.connect import cur, conn
from decimal import Decimal

def get(type: str, bat: int) -> Decimal:

    if type == "💵 Наличные":
        type = "cash"
    elif type == "🟩 USDT":
        type = "usdt"
    else:
        type = "bank"

    q = "SELECT marje FROM marje WHERE type=%s ORDER BY ABS(count - %s) LIMIT 1"
    cur.execute(q, (type, bat))
    result = cur.fetchone()
    if result:
        return float(result[0].quantize(Decimal('0.001')))
    else:
        return "No message found for the given type"

def get_view():
    q = "SELECT marje FROM marje WHERE type = 'view'"
    cur.execute(q)
    result = cur.fetchone()
    if result:
        return float(result[0].quantize(Decimal('0.001')))
    else:
        return "No message found for the given type"


def set_marje(type: str, count: float, marje: float):
    cur.execute("SELECT MAX(id) FROM marje")
    result = cur.fetchone()
    id = int(result[0])+1
    q = f"INSERT INTO marje (id, count, marje, type) VALUES ({id},{count}, {marje}, '{type}') ON CONFLICT (count, type) DO UPDATE SET marje = EXCLUDED.marje;"
    print(q)
    try:
        cur.execute(q)
        conn.commit()
    except psycopg2.Error as e:
        print("Error executing SQL query:", e)
        conn.rollback()
        return False



def get_all():
    q = "SELECT * FROM marje ORDER BY id"
    cur.execute(q)
    return cur.fetchall()
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

    q = "SELECT marje FROM marje WHERE count >= %s AND type = %s LIMIT 1"
    cur.execute(q, (bat, type))
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
    q = f"INSERT INTO marje (count, marje, type) VALUES ({count}, {marje}, '{type}') ON CONFLICT (count, type) DO UPDATE SET marje = {marje}"
    print(q)
    try:
        cur.execute(q)
        conn.commit()
    except psycopg2.Error as e:
        print("Error executing SQL query:", e)
        conn.rollback()
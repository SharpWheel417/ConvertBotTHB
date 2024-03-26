from database.connect import cur, conn
from decimal import Decimal

def get(type: str) -> Decimal:

    q = f"SELECT course FROM course WHERE type = '{type}'"
    cur.execute(q)
    result = cur.fetchone()
    if result:
        return float(result[0].quantize(Decimal('0.001')))
    else:
        return "No message found for the given type"


def set(type: str, count: float):
    if count is not None:
        q = f"INSERT INTO course (type, course) VALUES ('{type}', {count}) ON CONFLICT (type) DO UPDATE SET course = {count}"
        print(q)
        cur.execute(q)
        conn.commit()
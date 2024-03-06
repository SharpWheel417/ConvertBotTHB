from database.connect import cur
from decimal import Decimal

def get(type: str) -> Decimal:

    q = f"SELECT course FROM course WHERE type = '{type}'"
    cur.execute(q)
    result = cur.fetchone()
    if result:
        return float(result[0].quantize(Decimal('0.001')))
    else:
        return "No message found for the given type"
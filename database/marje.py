from database.connect import cur
from decimal import Decimal

def get(type: str, bat: int) -> str:

    if type == "💵 Наличные":
        type = "cash"
    elif type == "🟩 USDT":
        type = "usdt"
    else:
        type = "bank"

    q = "SELECT marje FROM user_marje WHERE count <= %s AND type = %s"
    cur.execute(q, (bat, type))
    result = cur.fetchone()
    if result:
        return result[0].quantize(Decimal('0.001'))
    else:
        return "No message found for the given type"
import re

def user_request(type:str, string: str) -> tuple:
    '''
    Вытыаскивает из текста запроса пользователя
    баты, рубли, usdt, курс и личный курс пользователя
    '''

    if type and type.group(1) == '🟩 USDT':

        exchange_match = re.search(r'Курс: (.+?) 📊', string)
        if exchange_match:
            exchange = exchange_match.group(1)

        bat_match = re.search(r'Для получения: (.+?) бат 🇹🇭', string)
        if bat_match:
            bat = bat_match.group(1)

        usdt_match = re.search(r'(\d+\.\d+) USDT', string)
        if usdt_match:
            usdt = usdt_match.group(1)

        return float(exchange), float(bat), float(usdt)

    if type and type.group(1) == '💵 Наличные':
        course_usd_match = re.search(r'Курс USD: (\d+\.\d+)\$', string)
        if course_usd_match:
            course_usd = course_usd_match.group(1)
        else:
            course_usd = "0"
            # Handle the case where no match was found for the USD course
            # For example, set a default value or raise an exception

        course_rub_match = re.search(r'Курс RUB: (\d+\.\d+)₽', string)
        if course_rub_match:
            course_rub = course_rub_match.group(1)
        else:
            course_rub="0"
            # Handle the case where no match was found for the RUB course
            # For example, set a default value or raise an exception

        bat_match = re.search(r'Для получения: (\d+\.\d+) бат', string)
        if bat_match:
            bat = bat_match.group(1)
        else:
            bat="0"
            # Handle the case where no match was found for the bat
            # For example, set a default value or raise an exception

        rub_usd_match = re.search(r'(\d+\.\d+) руб. или (\d+\.\d+) USD', string)
        if rub_usd_match:
            rub, usd = rub_usd_match.groups()
        else:
            rub="0"

        return float(course_usd), float(course_rub), float(bat), float(rub), float(usd)

    else:
        course_match = re.search(r'Курс: (\d+\.\d+)📊', string)
        if course_match:
            course = course_match.group(1)
        else:
            course = "0"
        # Handle the case where no match was found for the course

        bat_match = re.search(r'Для получения: (\d+\.\d+) бат', string)
        if bat_match:
            bat = bat_match.group(1)
        else:
            bat = "0"
        # Handle the case where no match was found for the bat

        rub_match = re.search(r'Вам необходимо: (\d+\.\d+) руб', string)
        if rub_match:
            rub = rub_match.group(1)
        else:
            rub="0"
        return float(course), float(rub), float(bat)


def admin_apply_user_name(string):
    username = re.search(r'@(\S+)', string).group(1)
    order_id_match = re.search(r'ID заказа: ([a-fA-F0-9-]+)', string)
    if order_id_match:
        order_id = order_id_match.group(1)
        print(order_id)
    return username, order_id
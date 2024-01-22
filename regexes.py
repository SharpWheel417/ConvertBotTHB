import re

def user_request(string):
    '''
    Вытыаскивает из текста запроса пользователя
    баты, рубли, usdt, курс и личный курс пользователя
    '''

    bat = re.search(r'(\d+(?:\.\d+)?) бат', string).group(1)
    rub = re.search(r'(\d+(?:\.\d+)?) руб', string).group(1)
    usdt = re.search(r'(\d+(?:\.\d+)?) USDT', string).group(1)
    trade_method = re.search(r'по курсу \((?:)?([^)]+)\)', string).group(1)

    last_two_numbers = re.findall(r'\b\d+\b', string)[-2:]
    if len(last_two_numbers) >= 2:
        rub_thb, thb_usdt = last_two_numbers
    else:
        rub_thb, thb_usdt = None, None

    return float(bat), float(rub), float(usdt), float(rub_thb), float(thb_usdt), trade_method


def admin_apply_user_name(string):
    username = re.search(r'@(\S+)', string).group(1)
    order_id_match = re.search(r'ID заказа: ([a-fA-F0-9-]+)', string)
    if order_id_match:
        order_id = order_id_match.group(1)
        print(order_id)
    return username, order_id
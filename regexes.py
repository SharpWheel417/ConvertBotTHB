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
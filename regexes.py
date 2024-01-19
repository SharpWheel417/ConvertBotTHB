import re

def user_request(str):
    '''
    Вытыаскивает из текста запроса пользователя
    баты, рубли, usdt, курс и личный курс пользователя
    '''

    string = str
    bat = re.search(r'(\d+) бат', string).group(1)
    rub = re.search(r'(\d+\.\d+) руб', string).group(1)
    usdt = re.search(r'\((\d+\.\d+) USDT', string).group(1)
    course_rub = re.search(r'по курсу (\d+\.\d+)', string).group(1)
    course_usdt = re.search(r'USDT: (\d+\.\d+)', string).group(1)

    return bat, rub, usdt, course_rub, course_usdt
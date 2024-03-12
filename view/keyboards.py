import database.db as db
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

def get_banks():
    banks = db.get_banks('rus')
    keyboard_buttons = []

    keyboard_buttons = []
    for i in range(0, len(banks), 2):
        cleaned_i1 = banks[i]
        cleaned_i2 = banks[i + 1] if i + 1 < len(banks) else []
        keyboard_buttons.append([cleaned_i1, cleaned_i2])

    keyboard_buttons.append(['🟰 Выбрать сумму'])

    return keyboard_buttons

def get_user_base():
    return ReplyKeyboardMarkup(
    [['5000', '7000', '10000', '15000', '20000'],
     ['25000', '30000', '50000', '100000', '300000'],
     ['Своя сумма','Узнать курс']],
    resize_keyboard=True
)

def get_admin_cancel():
    return ReplyKeyboardMarkup([['Отмена']], resize_keyboard=True)

def get_admin_base():
    return ReplyKeyboardMarkup(
            [['Изменить курс', 'Заказы'], ['Узнать курс', 'Узнать маржу', 'Статистика'], ['Калькулятор'],['Остановить переписку с юзером']],
            resize_keyboard=True
        )

def get_admin_calculate():
    return ReplyKeyboardMarkup([['Бат в руб', 'Бат в руб с маржой'], ['Бат в USDT', 'Бат в USDT с маржой'],['Рубль в бат', 'Рубль в бат с маржой'], ['Рубль в USDT', 'Рубль в USDT с маржой'],['USDT в бат', 'USDT в бат с маржой'],['USDT в рубль', 'USDT в рубль с маржой']], resize_keyboard=False)

def get_admin_stats():
    return ReplyKeyboardMarkup([['Выполненые', 'Выручка (руб)', 'Оценки', 'Всего пользователей'], ['Главное меню']], resize_keyboard=True)

def get_admin_orders():
    return ReplyKeyboardMarkup([['Запросы', 'В работе', 'Выполненные', 'Отмененные'], ['Главное меню']], resize_keyboard=True)

def get_admin_courses():
    return ReplyKeyboardMarkup(
            [['Изменить курс рубля', 'Изменить курс usdt']],
            resize_keyboard=True)

def get_user_complete():
    return ReplyKeyboardMarkup([['Поставить оценку'], ['Выбрать сумму']], resize_keyboard=True)

def get_user_marks():
    return ReplyKeyboardMarkup([['1', '2', '3', '4', '5']], resize_keyboard=True)

def get_admin_inline_buttons():
    cancle_button = InlineKeyboardButton('Отклонить', callback_data="cancle")

    complete_button = InlineKeyboardButton("Взять в работу", callback_data='apply')

    keyboard = InlineKeyboardMarkup([[cancle_button], [complete_button]])

    return keyboard

def get_admin_inline_buttons_in_progress():
    cancle_button = InlineKeyboardButton('Отклонить', callback_data="cancle")

    complete_button = InlineKeyboardButton("Выполнен", callback_data='complete')

    keyboard = InlineKeyboardMarkup([[cancle_button], [complete_button]])

    return keyboard


def request_user():
    share_location_button = KeyboardButton("Посмотреть банкоматы и сообщить свое местоположение 🏧", request_location=True)
    return ReplyKeyboardMarkup([[share_location_button], ["🟰 Выбрать сумму"], ["Не делиться ⛔️"]], resize_keyboard=True)
import db
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def get_banks():
    banks = db.get_banks('rus')
    keyboard_buttons = []

    keyboard_buttons = []
    for i in range(0, len(banks), 2):
        cleaned_i1 = banks[i]
        cleaned_i2 = banks[i + 1] if i + 1 < len(banks) else []
        keyboard_buttons.append([cleaned_i1, cleaned_i2])

    keyboard_buttons.append(['Другая сумма'])

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
            [['Изменить курс', 'Заказы'], ['Узнать курс', 'Статистика'], ['Остановить переписку с юзером']],
            resize_keyboard=True
        )

def get_admin_stats():
    return ReplyKeyboardMarkup([['Выполненые', 'Выручка (руб)', 'Оценки', 'Всего пользователей'], ['Главное меню']], resize_keyboard=True)

def get_admin_orders():
    return ReplyKeyboardMarkup([['Запросы', 'В работе', 'Выполненные', 'Отмененные'], ['Главное меню']], resize_keyboard=True)
    
def get_admin_courses():
    return ReplyKeyboardMarkup(
            [['Изменить курс рубля', 'Изменить курс USDT'], ["Изменить процент маржи"], ['Главное меню']],
            resize_keyboard=True
        )

def get_user_complete():
    return ReplyKeyboardMarkup([['Оставить отзыв'], ['Поставить оценку'], ['Выбрать сумму']], resize_keyboard=True)

def get_user_marks():
    return ReplyKeyboardMarkup([['1', '2', '3', '4', '5']], resize_keyboard=True)

def get_admin_inline_buttons():
    cancle_button = InlineKeyboardButton('Отклонить', callback_data="cancle")
            
    complete_button = InlineKeyboardButton("Взять в работу", callback_data='apply')

    keyboard = InlineKeyboardMarkup([[cancle_button], [complete_button]])

    return keyboard
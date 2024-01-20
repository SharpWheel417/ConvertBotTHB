import db
from telegram import ReplyKeyboardMarkup

def get_banks():
    banks = db.get_banks('rus')
    keyboard_buttons = []
    for i in banks:
        cleaned_i = [value.strip() for value in i]
        keyboard_buttons.append(cleaned_i)
    return keyboard_buttons

def get_user_base():
    return ReplyKeyboardMarkup(
            [['1000', '2000'], ['3000', '4000'], ['Своя сумма','Узнать курс']],
            resize_keyboard=True
        )

def get_admin_cancel():
    return ReplyKeyboardMarkup([['Отмена']], resize_keyboard=True)

def get_admin_base():
    return ReplyKeyboardMarkup(
            [['Изменить курс рубля', 'Изменить курс USDT'], ["Изменить процент маржи", 'Узнать курс'], ['Остановить переписку с юзером']],
            resize_keyboard=True
        )
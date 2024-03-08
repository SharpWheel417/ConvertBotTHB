from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, ContextTypes
from datetime import datetime
from typing import Any, Coroutine

import parsing.commex as commex, parsing.bitazza as bitazza
import database.get_message as get_message
import database.course as c

#####   ФУНКЦИЯ ПАРСИНГА КУРСА   ####

file_name = "course_THB_data.txt"

def parse_course(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.bot.send_message(chat_id=update.effective_chat.id, text="Получение курса...")

    rub = commex.get_average()
    c.set('rub', rub)
    print("Average:", rub)

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Рубль: {rub}\nПолучаем Bitazza....\n(долго, может больше 2 минут)")

    thb = bitazza.get_currency()
    print("Новый курс битаззы: ", thb)
    if thb == 'error':
        print("Ошибка парсинга битаззы")
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Не смогли получить Bitazza")
        return
    else:
        c.set('thb', thb)


    txt = get_message.get_mess('parse_course', True).format(thb=thb, rub=rub)
    context.bot.send_message(chat_id=update.effective_chat.id, text=txt)


    ###Запись логов в файл
    file = open(file_name, 'a')
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file.write(f"Date: {current_date}, THB: {thb}, \n RUB: {rub}")
    print("Данные успешно записаны в файл:", file_name)
    file.close()
    print("Курс сейча: ", thb)

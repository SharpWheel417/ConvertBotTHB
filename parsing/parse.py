from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, ContextTypes
from datetime import datetime
from typing import Any, Coroutine
import asyncio
import requests

import config
import parsing.commex as commex, parsing.bitazza as bitazza
import database.get_message as get_message
import database.course as c

#####   ФУНКЦИЯ ПАРСИНГА КУРСА   ####

file_name = "course_THB_data.txt"

def parse_course(update: Update, context: ContextTypes.DEFAULT_TYPE):

    fine = False

    sendmess(update, "Начинаем парсинг")


    rub = commex.get_average()
    c.set('rub', rub)
    print("Average:", rub)
    # context.bot.send_message(chat_id=update.effective_chat.id, text=f"Рубль: {rub}\nПолучаем Bitazza....\n(долго, может больше 2 минут)")
    sendmess(update, f"Рубль: {rub}\nПолучаем Bitazza....\n(долго, может больше 2 минут)")

    thb = bitazza.get_currency()
    print("Новый курс битаззы: ", thb)
    if thb == 'error':
        sendmess(update, "Не смогли получить Bitazza")
        print("Ошибка парсинга битаззы")
        return
    else:
        sendmess(update, f"Получили Bitazza: {thb}")
        c.set('thb', thb)
        fine=True

    txt = get_message.get_mess('parse_course', True).format(thb=thb, rub=rub)
    sendmess(update, txt)

    ###Запись логов в файл
    file = open(file_name, 'a')
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file.write(f"Date: {current_date}, THB: {thb}, \n RUB: {rub}")
    print("Данные успешно записаны в файл:", file_name)
    file.close()
    print("Курс сейча: ", thb)

    return fine


def sendmess(update: Update, txt):
    url = f"https://api.telegram.org/bot{config.pills}/sendMessage?chat_id={update.effective_chat.id}&text={txt}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

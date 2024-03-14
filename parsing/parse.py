
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

def parse_course():

    fine = False

    sendmess("Начинаем парсинг")


    rub = commex.get_average()
    c.set('rub', rub)
    print("Average:", rub)
    # context.bot.send_message(chat_id=ffective_chat.id, text=f"Рубль: {rub}\nПолучаем Bitazza....\n(долго, может больше 2 минут)")
    sendmess(f"Рубль: {rub}\nПолучаем Bitazza....\n(долго, может больше 2 минут)")

    thb = bitazza.get_currency()
    print("Новый курс битаззы: ", thb)
    if thb == 'error':
        sendmess("Не смогли получить Bitazza")
        print("Ошибка парсинга битаззы")
        return
    else:
        sendmess(f"Получили Bitazza: {thb}")
        c.set('thb', thb)
        fine=True

    txt = get_message.get_mess('parse_course', True).format(thb=thb, rub=rub)
    sendmess(txt)

    ###Запись логов в файл
    file = open(file_name, 'a')
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file.write(f"Date: {current_date}, THB: {thb}, \n RUB: {rub}")
    print("Данные успешно записаны в файл:", file_name)
    file.close()
    print("Курс сейча: ", thb)

    return fine


def sendmess(txt):
    url = f"https://api.telegram.org/bot{config.pills}/sendMessage?chat_id=-4126423671&text={txt}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message. Status code: {response.status_code}\n{response.text}")

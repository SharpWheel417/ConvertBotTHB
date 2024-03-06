from telegram import Bot, Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
import schedule, time, re, tracemalloc, logging
tracemalloc.start()
import uuid, threading
from datetime import datetime

import model.convert as convert, parsing.commex as commex, database.db as db, model.regexes as regexes, parsing.geo as geo, view.keyboards as keyboards, parsing.bitazza as bitazza, model.calc as calc, database.example as example

import database.get_message as get_message
import database.marje as mj
import database.course as c

from config import pills

BOT_TOKEN = pills

# ADMIN_ID = [1194700554, 6920037183]
# ADMIN_ID = [1194700554]
ADMIN_ID = []
CHANEL_ID = 'channel4exchange_thai'
file_name = "course_THB_data.txt"


def parse_course(update: bool):

    new_course_rub = commex.get_average()
    global course_rub, course_THB, admin_course_rub, user_course_rub
    admin_course_rub = new_course_rub
    user_course_rub = new_course_rub
    course_rub = new_course_rub
    print("Average:", course_rub)

    new_course_THB = bitazza.get_currency()
    print("Новый курс битаззы: ", new_course_THB)
    if new_course_THB == 'error':
        print("Ошибка парсинга битаззы")
        return
    global user_course_THB, admin_course_THB
    # if update is False:
    #     if(float(new_course_THB)<user_course_THB):
    #         user_course_THB = new_course_THB
    #     admin_course_THB = new_course_THB
    #     course_THB = new_course_THB
    # else:
    user_course_THB = new_course_THB
    admin_course_THB = new_course_THB
    course_THB = new_course_THB

    ###Запись логов в файл
    file = open(file_name, 'a')
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file.write(f"Date: {current_date}, course_THB: {course_THB}, admin_course_THB: {admin_course_THB}, user_course_THB: {user_course_THB}, course_THB: {course_THB}\n admin_course_rub: {admin_course_rub}, user_course_THB: {user_course_rub}\n")
    print("Данные успешно записаны в файл:", file_name)
    file.close()
    print("Курс сейча: ", course_THB)

##### РАСКОМЕНТИРОВАТЬ
# thread_parse = threading.Thread(target=parse_course(True))
# thread_parse.start()

lock = threading.Lock()

def run_scheduler():
    # Запуск шедулера каждый час

    ##### РАСКОМЕНТИРОВАТЬ
    # schedule.every(1).hour.do(lambda: run_with_lock(parse_course, False))

    # schedule.every().day.at('10:00').do(lambda: run_with_lock(parse_course, True))

    # Бесконечный цикл для запуска шедулера
    while True:
        schedule.run_pending()
        time.sleep(10)

def run_with_lock(func, arg):
    with lock:
        func(arg)

# Создание и запуск потока для шедулера
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

selected_user_id = None


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def count_thb_usdt_user(bat):
    global user_course_THB, usdt_marje
    return round(float((float(bat)/(float(round(user_course_THB, 2))*(2-usdt_marje)))),2)


##### Команда /user для админа ####
async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in ADMIN_ID:
        # Сохраните выбранный идентификатор пользователя
        user_id = update.message.text.split('/user ')[1]
        global selected_user_id
        selected_user_id = user_id
        await update.message.reply_text(f'Выбран пользователь с идентификатором {selected_user_id}. Теперь вы можете отправить сообщение.')
    else:
        await update.message.reply_text('Извините, вы не авторизованы.')

##### Команда /user для админа ####
async def new_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id in ADMIN_ID:
        text = update.message.text
        new_text = text.replace("/newtext", "")
        db.change_logo_text(new_text)



### Комманда Старт ###
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_course_rub, user_course_THB
    user_id = update.effective_user.id
    username = update.effective_user.username
    user_first_name = update.effective_user.first_name

    db.add_new_user(user_id, username, user_first_name)

    db.set_state(user_id, '0')
    db.set_bats(user_id, '0')

    ### Админ ###
    if user_id in ADMIN_ID:
        #admin panel
        await context.bot.send_message(chat_id=update.effective_chat.id, text=get_message.get_mess("hello_message", True), reply_markup=keyboards.get_admin_base())

    ### Юзер ###
    else:
        more_button = InlineKeyboardButton('Больше информации', callback_data="more_inf")

        reviews_button = InlineKeyboardButton('Прочитать отзывы', url=f"{db.get_review_link()}")

        keyboard = InlineKeyboardMarkup([[more_button], [reviews_button]])

        await context.bot.send_message(chat_id=update.effective_chat.id, text=db.get_logo_text(), reply_markup=keyboard)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=get_message.get_mess('hello_message', False), reply_markup=keyboards.get_user_base())



### Обычное сообщение ####
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global user_course_THB, course_THB, user_course_rub, course_rub, usdt_marje, cash_marje, marje, admin_course_rub, admin_course_THB

    text = update.message.text
    global selected_user_id
    user_id = update.effective_user.id
    if user_id in ADMIN_ID:

        if text == 'Главное меню':
            await context.bot.send_message(chat_id=update.effective_chat.id, text='На главную', reply_markup=keyboards.get_admin_base())

        if text == 'Заказы':
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Заказы:", reply_markup=keyboards.get_admin_orders())

        ### КАЛЬКУЛЯТОР ###
        if text == 'Калькулятор':
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Калькулятор:", reply_markup=keyboards.get_admin_calculate())


        ##Для админов
        if text == "Узнать курс":
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс с Bitazza USDT/THB  : {admin_course_THB} \nКурс Bitazza минимальный за день: {user_course_THB} \nКурс Bitazza с процентом (0.02): {admin_course_THB*(2-0.02)} \nКурс Bitazza для пользователя (с маржой)  : {user_course_THB*(2-marje)} \n\nКурс рубля к бату: {round(admin_course_rub/admin_course_THB,2)}\n\nКурс rub для пользователей: {user_course_rub} \nКурс rub для пользователей (с маржой): {round(user_course_rub*float(marje),2)} \n Процент маржи для банкоа : {round((marje*100),2)} % || {marje} \nПроцент маржи для USDT: {round(float(usdt_marje)*100, 2)} % || {usdt_marje}  \nПроцент маржи Наличка: {round(float(cash_marje)*100, 2)} % || {cash_marje}")
            return
        ##Для админов
        if text == "Остановить переписку с юзером":
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Переиска с юзером {selected_user_id} остановлена")
            selected_user_id = None
            return

        ##Для админов
        if selected_user_id:
            chat_id = db.find_chat_id(selected_user_id)

            if chat_id:
                await context.bot.send_message(chat_id=chat_id, text=f'Ответ администратора: {text}')
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"С этим {username} не зарегистрирован чат")


    ### Для юзеров ###
    ##################
    if user_id not in ADMIN_ID:

        ### Для юзеров ###
        if text == "Узнать курс":

            user_course_rub = float(user_course_rub)
            user_course_THB = float(user_course_THB)
            # marje = float(marje)

            thb = c.get('thb')
            rub = c.get('rub')
            m = mj.get_view()
            course_rub_marje = rub * m
            course_thb_marje = thb * (2 - m)
            course_thb_rub = round(course_rub_marje / course_thb_marje, 2)
            course_thb_value = round(course_thb_marje, 2)



            message_text = get_message.get_mess("course", False).format(course_thb_value=course_thb_value, course_thb_rub=course_thb_rub)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text, reply_markup=keyboards.get_user_base())
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Маржа: {m}, Курс THB: {thb}, Курс RUB: {rub}")
            return

        elif db.get_state(user_id) == 'ожидание оценки':
            # db.set_mark(complete[user_id], text)

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Благодарим за оценку 👍", reply_markup=keyboards.get_user_base())

            db.set_state(user_id, '0')
            return

        # if user_id in complete and complete[user_id] is not None:

        #      if text == 'Поставить оценку':
        #         db.set_state(user_id, 'ожидание оценки')
        #         await context.bot.send_message(chat_id=update.effective_chat.id, text='Оцените работу нашего сервиса от 1 до 5 баллов', reply_markup=keyboards.get_user_marks())
        #         return

        #      if text == 'Оставить отзыв':
        #         db.set_state(user_id, 'ожидание отзыва')
        #         await context.bot.send_message(chat_id=update.effective_chat.id, text='Напишиет отзыв на нашу работу', reply_markup=None)
        #         return


        if text == "Своя сумма":
            await context.bot.send_message(chat_id=update.effective_chat.id, text=get_message.get_mess("my_sum", False))
            return

        if text == "Поделиться геолокацией":
            geo_handler()
        if text == "Не делиться ⛔️":
            db.set_state(user_id, '0')
            await context.bot.send_message(chat_id=update.effective_chat.id, text=get_message.get_mess("send_geo", False), reply_markup=keyboards.get_user_base())
            return

        ### Для юзеров ###
        if text == "🟰 Выбрать сумму":
            db.set_state(user_id, '0')

            await context.bot.send_message(chat_id=update.effective_chat.id, text=get_message.get_mess("take_sum", False), reply_markup=keyboards.get_user_base())
            return

        ### Для юзеров ###
        ### После выбора суммы ждем когда пользователь выберет способ оплаты ###
        elif (db.get_state(user_id) == 'ожидание_выбора_способа_оплаты'):

            if text in db.get_banks('rus'):

                if text == '🟩 USDT':
                    m = mj.get('usdt', db.get_bats(user_id))
                    print(m)
                if text == '💵 Наличные':
                    m = mj.get('cash', db.get_bats(user_id))
                    print(m)
                else:
                    m = mj.get('bank',db.get_bats(user_id))
                    print(m)

                ## Получаем данные из бд
                c_thb = c.get('thb')
                c_rub = c.get('rub')
                u_bat = db.get_bats(user_id)

                rub_course = commex.get_by_trade_method(text, u_bat, c_thb, c_rub, m)

                rub =  u_bat*((rub_course*m)/(c_thb*(2-m)))
                usdt =  u_bat/(2-m)


                # Создание кнопки "Запросить"
                request_button = InlineKeyboardButton('Разместить заказ', callback_data="request")

                txt = get_message.get_mess("usdt", False).format(usdt=round(usdt,2), course_thb=c_thb*(2-m), bat=u_bat)

                # Создание клавиатуры с кнопкой "Запросить"
                keyboard = InlineKeyboardMarkup([[request_button]])
                await context.bot.send_message(chat_id=update.effective_chat.id, text=txt, reply_markup=keyboard)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Маража {m}")
                return
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=get_message.get_mess("please", False))
                return


        elif text.isdigit():

            if db.get_state(user_id) == 'ожидание оценки':
                db.set_state(user_id, '0')
                return

            db.set_state(user_id, 'ожидание_выбора_способа_оплаты')
            db.set_bats(user_id, float(text))

            keyboard = ReplyKeyboardMarkup(keyboards.get_banks(), resize_keyboard=True)

            await context.bot.send_message(chat_id=update.effective_chat.id, text=get_message.get_mess("please", False), reply_markup=keyboard)

        else:
            if db.check_request:
                if selected_user_id != None:
                    sel_chat = db.find_chat_id(selected_user_id)
                    if update.effective_chat.id == int(sel_chat):
                        username = db.find_name(update.effective_chat.id)
                        await context.bot.send_message(chat_id=ADMIN_ID[0], text=f'Текст от юзера @{username}: {text}')

## Кнопки ###
async def button_callback(update: Update, context: CallbackContext, *args, **kwargs):

    global admin_course_THB, admin_course_rub
    query = update.callback_query
    # Получаем callback_data из нажатой кнопки
    callback_data = update.callback_query.data


    if callback_data == 'more_inf':

        await context.bot.send_message(chat_id=query.message.chat_id, text=db.get_info_text(), parse_mode='Markdown', disable_web_page_preview=True)

    if callback_data == 'apply':
        ##Меняем кнопки###

        cancle_button = InlineKeyboardButton('Отклонить', callback_data="cancle")

        complete_button = InlineKeyboardButton("Выполнен", callback_data='complete')

        keyboard = InlineKeyboardMarkup([[cancle_button], [complete_button]])

        await context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=keyboard)

        username, order_id = regexes.admin_apply_user_name(query.message.text)
        chat_id = db.get_chat_id(username)

        ## Отправляем сообщение пользователю
        await context.bot.send_message(chat_id=chat_id, text=get_message.get_mess("take_order", False))

        db.set_progress(order_id)

    if callback_data == 'complete':

        username, order_id = regexes.admin_apply_user_name(query.message.text)
        chat_id = db.get_chat_id(username)

        for id in ADMIN_ID:
            await context.bot.send_message(chat_id=id, text=f'Заказ {order_id} \nДля @{username} \nВыполнен!', reply_markup=None)

        await context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=None)

        url_button = InlineKeyboardButton("Написать отзыв", url="https://t.me/channel4exchange_thai/20")
        board = InlineKeyboardMarkup([[url_button]])

        ## Отправляем сообщение пользователю
        txt = get_message.get_mess("ready", False).format(order_id=order_id)
        await context.bot.send_message(chat_id=chat_id, text=txt, reply_markup=keyboards.get_user_complete())

        await context.bot.send_message(chat_id=chat_id, text=get_message.get_mess("text_for_order", False), reply_markup=board)

        # complete[int(chat_id)] = order_id

        db.set_complete(order_id)

    if callback_data == 'cancle':

        username, order_id = regexes.admin_apply_user_name(query.message.text)
        chat_id = db.get_chat_id(username)

        for id in ADMIN_ID:
            await context.bot.send_message(chat_id=id, text=f'Заказ {order_id} \nДля @{username} \nОтменен', reply_markup=None)

        await context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=None)

        db.set_cancle(order_id)


    ### Кнопка "Запросить" ###
    if callback_data == 'request':

        # Отправляем запрос на получение бат
        await context.bot.send_message(chat_id=query.message.chat_id, text=get_message.get_mess("request_user", False), reply_markup=keyboards.request_user())

        ## Парсим из текста запроса пользоавтеля нужные данные
        bat, rub, usdt, rub_thb, thb_usdt, trade_method = regexes.user_request(query.message.text)

        ## Получаем чисту цену
        clean_count = convert.clean(bat, admin_course_THB, admin_course_rub)
        gain = float(rub)-float(clean_count)
        gain_bat = round(gain/ (admin_course_rub/admin_course_THB),2)
        gain_usdt = round(gain/admin_course_rub ,2)

        best_course, best_trade = commex.get_best(float(rub))

        ##Создаем ID заказа###
        ids = str(uuid.uuid4())

        if db.check_order_id(ids):
            ids = str(uuid.uuid4())

        user_want_usdt = 10

        mess = f'''
        ID заказа: {ids}
@{query.from_user.username} думает получить {bat} бат через {trade_method}

Курс для клиента: {rub_thb} ({thb_usdt} бат/USDT ; {round(rub_thb*thb_usdt, 2)} руб/USDT)

Реальный Курс: {round(admin_course_rub/admin_course_THB, 2)} ({admin_course_THB} бат/USDT ; {admin_course_rub} руб/USDT)

Сумма оплаты клиентом: {rub} руб. либо {round(rub/(thb_usdt*rub_thb), 2)} USDT

Сумма реальная: {clean_count} руб. ({round(clean_count/admin_course_rub, 2)} USDT)

Зарабатываем с этого: {round(gain,2)} руб или {round(gain_bat,2)} бат  или {round(gain_usdt, 2)} USDT

Bitazza для админа: {admin_course_THB}

Самый выгодный способ платежа: {best_trade} {best_course} руб/USDT, {round(best_course/admin_course_THB, 2)} руб/ТНВ'''

        db.request_on(query.message.chat_id)

        cancle_button = InlineKeyboardButton('Отклонить', callback_data="cancle")
        apply_button = InlineKeyboardButton('Взять в работу', callback_data="apply")
        # Создание клавиатуры с кнопкой "Запросить"
        keyboard = InlineKeyboardMarkup([[cancle_button], [apply_button]])

        for chat_id in ADMIN_ID:
            await context.bot.send_message(chat_id=chat_id, text=mess, reply_markup=keyboard)

        ### Записываем данные в базу данных ###
        db.create_order(ids, query.from_user.username, float(rub), clean_count, usdt, rub_thb, marje, gain, trade_method, bat, user_want_usdt)

    return True







##Отправка геолокации
# async def handle_geo(update: Update, context: CallbackContext):
#     location = update.message.location
#     text = geo.geocoder(location.latitude, location.longitude, update.message.chat_id)
#     for chat_id in ADMIN_ID:
#         ### Текст с адресом пользователя ###
#         await context.bot.send_message(chat_id=chat_id, text=text)
#         ### Выводит карту с геопозицией пользователя ####
#         await context.bot.send_location(chat_id=chat_id, longitude=location.longitude, latitude=location.latitude)

















async def error_handler(update, context):
    # Log the error or handle it in some way
    print(f"An error occurred: {context.error}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CallbackQueryHandler(button_callback))

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    user_handler = CommandHandler('user', user_message)
    application.add_handler(user_handler)

    newtext_handler = CommandHandler('newtext', new_text_message)
    application.add_handler(newtext_handler)

    message_handler = MessageHandler(filters.TEXT, handle_message)
    application.add_handler(message_handler)

    geo_handler = MessageHandler(filters.LOCATION, geo.handle_geo(Update, ContextTypes.DEFAULT_TYPE, ADMIN_ID))
    application.add_handler(geo_handler)


    application.run_polling()

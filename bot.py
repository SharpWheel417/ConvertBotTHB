from telegram import Bot, Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
import schedule, time, re, tracemalloc, logging
tracemalloc.start()
import uuid, threading
from datetime import datetime
import functools

import model.convert as convert, parsing.commex as commex, database.db as db, model.regexes as regexes, parsing.geo as geo, view.keyboards as keyboards, parsing.bitazza as bitazza, model.calc as calc, database.example as example

import database.get_message as get_message
import database.marje as mj
import database.course as c
import parsing.parse as p

import view.marje as vm

from config import battle_life

BOT_TOKEN = battle_life

ADMIN_ID = [1194700554, 6920037183]
# ADMIN_ID = [1194700554]
# ADMIN_ID = []
CHANEL_ID = 'channel4exchange_thai'

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
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс с Bitazza USDT/THB  : {c.get('thb')} \n \nКурс Bitazza с процентом (0.02): {admin_course_THB*(2-0.02)} \nКурс Bitazza для пользователя (с маржой)  : {user_course_THB*(2-marje)} \n\nКурс рубля к бату: {round(admin_course_rub/admin_course_THB,2)}\n\nКурс rub для пользователей: {user_course_rub} \nКурс rub для пользователей (с маржой): {round(user_course_rub*float(marje),2)} \n Процент маржи для банкоа : {round((marje*100),2)} % || {marje} \nПроцент маржи для USDT: {round(float(usdt_marje)*100, 2)} % || {usdt_marje}  \nПроцент маржи Наличка: {round(float(cash_marje)*100, 2)} % || {cash_marje}")
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

            # user_course_rub = float(user_course_rub)
            # user_course_THB = float(user_course_THB)
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

                ## Получаем данные из бд
                c_thb = c.get('thb')
                c_rub = c.get('rub')
                u_bat = db.get_bats(user_id)

                # usdt =  u_bat/(2-m)

                if text == '🟩 USDT':
                    m = mj.get('usdt', db.get_bats(user_id))
                    client_c_thb = round(c_thb*(2-m),2)
                    usdt =  u_bat/client_c_thb
                    txt = get_message.get_mess("usdt", False).format(usdt=round(usdt,2), course_thb=client_c_thb, bat=u_bat)

                elif text == '💵 Наличные':
                    m = mj.get('cash', db.get_bats(user_id))
                    rub =  u_bat*((c_rub*m)/(c_thb*(2-m)))
                    usdt =  u_bat/(c.get('thb')*(2-m))
                    txt = get_message.get_mess("cash", False).format(course_rub=round(c_rub*(m),2), course_usdt=round(c_thb*(2-m),2), bat=u_bat, rub=round(rub,2), usdt=round(usdt,2))

                else:
                    m = mj.get('bank',db.get_bats(user_id))
                    course_thb_bat = c_rub*(m)/c_thb*(2-m)
                    rub_course = commex.get_by_trade_method(text, u_bat, c_thb, c_rub, m)
                    rub =  u_bat*((float(rub_course)*m)/(c_thb*(2-m)))
                    usdt =  u_bat/(2-m)
                    txt = get_message.get_mess("bank", False).format(course_thb_bat=round(course_thb_bat,2), rub=round(rub,2), bat=u_bat, trade_method=text)


                # Создание кнопки "Запросить"
                request_button = InlineKeyboardButton('Разместить заказ', callback_data="request")

                # txt = get_message.get_mess("usdt", False).format(usdt=round(usdt,2), course_thb=c_thb*(2-m), bat=u_bat)

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


        ##Создаем ID заказа###
        ids = str(uuid.uuid4())
        # if db.check_order_id(ids):
        #     ids = str(uuid.uuid4())


        trade_method = re.search(r'по курсу\s+(.+)', query.message.text)
        if trade_method and trade_method.group(1) == '🟩 USDT':

            course, bat, usdt = regexes.user_request(trade_method, query.message.text)
            c_thb = c.get('thb')
            real_usdt = bat/c_thb
            gain_usdt = usdt - real_usdt
            gain_bat = gain_usdt*c_thb

            rub = bat*(c.get('rub')/c_thb)


            best_trade_method = commex.get_best(rub)
            txt = get_message.get_mess('order_usdt', True).format(id=ids,
                                                                username=query.from_user.username,
                                                                bat=bat,
                                                                client_course_thb=course,
                                                                real_course_thb=c_thb,

                                                                client_usdt=usdt,
                                                                real_usdt=round(real_usdt,2),
                                                                gain_bat=round(gain_bat,2),
                                                                gain_usdt=round(gain_usdt,2),
                                                                best_trade_method=best_trade_method[1],
                                                                best_course_rub=best_trade_method[0],
                                                                best_course_thb_rub="0")

        elif trade_method and trade_method.group(1) == '💵 Наличные':
            course_usdt, course_rub, bat, rub, usdt = regexes.user_request(trade_method, query.message.text)

            client_thb_rub = float(course_rub)/float(course_usdt)

            real_course_thb_rub = (c.get('rub')/c.get('thb'))
            real_rub = bat*real_course_thb_rub
            real_usdt = bat/c.get('thb')

            gain_rub = rub-round(real_rub,2)
            gain_usdt = usdt - round(real_usdt,2)

            best_trade_method = commex.get_best(rub)

            txt = get_message.get_mess('order_cash', True).format(id=ids,
                                                                username=query.from_user.username,
                                                                bat=bat,
                                                                client_thb_rub=round(client_thb_rub,2),
                                                                client_rub=round(course_rub,2),
                                                                real_course_thb_rub=round(real_course_thb_rub,2),
                                                                real_course_rub=c.get('rub'),
                                                                rub=rub,
                                                                usdt=usdt,
                                                                real_rub=round(real_rub,2),
                                                                real_usdt=round(real_usdt,2),
                                                                gain_rub=round(gain_rub,2),
                                                                gain_usdt=round(gain_usdt,2),
                                                                course_thb=c.get('thb'),
                                                                best_trade=best_trade_method[1],
                                                                best_course_rub=best_trade_method[0])



        else:
            course, rub, bat = regexes.user_request(trade_method, query.message.text)
            usdt = rub/c.get('rub')

            real_rub = bat*(c.get('rub')/c.get('thb'))
            real_usdt = bat/c.get('thb')

            gain_rub = rub-real_rub
            gain_usdt = usdt-real_usdt

            best_trade_method = commex.get_best(rub)

            real_course_thb_rub = c.get('rub')/c.get('thb')

            txt = get_message.get_mess('order_bank', True).format(id=ids,
                                                                username=query.from_user.username,
                                                                bat=bat,
                                                                trade_method=trade_method.group(1),
                                                                client_course_rub=course,
                                                                client_course_thb_rub=course,
                                                                rub=round(rub,2),
                                                                usdt=round(usdt,2),
                                                                real_rub=round(real_rub,2),
                                                                real_usdt=round(real_usdt,2),
                                                                gain_rub=round(gain_rub,2),
                                                                real_course_thb_rub=round(real_course_thb_rub,2),
                                                                gain_usdt=round(gain_usdt,2),
                                                                c_thb=c.get('thb'),
                                                                best_trade={best_trade_method[0]},
                                                                best_course={best_trade_method[1]}
                                                                )

        db.request_on(query.message.chat_id)

        cancle_button = InlineKeyboardButton('Отклонить', callback_data="cancle")
        apply_button = InlineKeyboardButton('Взять в работу', callback_data="apply")
        # Создание клавиатуры с кнопкой "Запросить"
        keyboard = InlineKeyboardMarkup([[cancle_button], [apply_button]])

        await context.bot.send_message(chat_id=query.message.chat_id, text=get_message.get_mess("request_user", False), reply_markup=keyboards.request_user())

        for chat_id in ADMIN_ID:
            await context.bot.send_message(chat_id=chat_id, text=txt, reply_markup=keyboard)

        ### Записываем данные в базу данных ###
        # db.create_order(ids, query.from_user.username, float(rub), clean_count, usdt, rub_thb, marje, gain, trade_method, bat, user_want_usdt)

    return True







##Отправка геолокации
async def handle_geo(update: Update, context: CallbackContext):
    location = update.message.location
    text = geo.geocoder(location.latitude, location.longitude, update.message.chat_id)
    for chat_id in ADMIN_ID:
        ### Текст с адресом пользователя ###
        await context.bot.send_message(chat_id=chat_id, text=text)
        ### Выводит карту с геопозицией пользователя ####
        await context.bot.send_location(chat_id=chat_id, longitude=location.longitude, latitude=location.latitude)

############ПАРСИНГ
async def parse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in ADMIN_ID:
        await p.parse_course(update, context)  # Ensure to await the coroutine

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Вы не админ")


async def runParser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in ADMIN_ID:
    ##### РАСКОМЕНТИРОВАТЬ
        lock = threading.Lock()

        def run_scheduler(update, context):
            # Запуск шедулера каждый час
            schedule.every(1).hour.do(functools.partial(run_with_lock, p.parse_course, update, context, False))

            # Бесконечный цикл для запуска шедулера
            while True:
                schedule.run_pending()
                time.sleep(10)

        def run_with_lock(func, *args):
            with lock:
                func(*args)

        # Создание и запуск потока для шедулера
        scheduler_thread = threading.Thread(target=run_scheduler, args=(update, context))
        scheduler_thread.start()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Парсинг каждый час запущен!")


### ИЗМЕНЕНИЕ МАРЖИ
async def changeMarje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in ADMIN_ID:
        await vm.change_marje(update, context)

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Вы не админ")





async def error_handler(update, context):
    # Log the error or handle it in some way
    print(f"An error occurred: {context.error}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CallbackQueryHandler(button_callback))

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    ##Сразу же парсим курс
    parse_handler = CommandHandler('parse', parse)
    application.add_handler(parse_handler)

    ##Запускает шедулер каждый час парсинга
    run_handler = CommandHandler('run', runParser)
    application.add_handler(run_handler)

    ##Запускает шедулер каждый час парсинга
    change_marje_handler = CommandHandler('m', changeMarje)
    application.add_handler(change_marje_handler)

    ##Выбрать юзера для переписки
    user_handler = CommandHandler('user', user_message)
    application.add_handler(user_handler)

    newtext_handler = CommandHandler('newtext', new_text_message)
    application.add_handler(newtext_handler)

    message_handler = MessageHandler(filters.TEXT, handle_message)
    application.add_handler(message_handler)

    ##Поделиться геолокацией
    geo_handler = MessageHandler(filters.LOCATION, handle_geo)
    application.add_handler(geo_handler)


    application.run_polling()

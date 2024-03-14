from telegram import Bot, Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
import schedule, time, re, tracemalloc, logging
tracemalloc.start()
import uuid, threading
from datetime import datetime
import functools
import asyncio
import concurrent.futures

import model.convert as convert, parsing.commex as commex, database.db as db, model.regexes as regexes, parsing.geo as geo, view.keyboards as keyboards, parsing.bitazza as bitazza

import view.calculate as calc
import database.get_message as get_message
import database.marje as mj
import database.course as c
import database.state as s
import parsing.parse as p

import view.marje as vm
import view.course as vc
import view.user_bank as vu
import view.stats as vs
import view.orders as vo
import view.changeCourse as vcc

from config import pills

BOT_TOKEN = pills

ADMIN_ID = [1194700554, 6920037183]
# ADMIN_ID = [1194700554]
# ADMIN_ID = []
CHANEL_ID = 'channel4exchange_thai'

selected_user_id = None

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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
    print(update._effective_chat.id)
    if update.effective_user.last_name is None:
        user_fio = update.effective_user.first_name
    else:
        user_fio = update.effective_user.first_name + " " + update.effective_user.last_name

    db.add_new_user(user_id, username, user_fio)

    s.set_state(user_id, '0')
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

    text = update.message.text
    global selected_user_id
    user_id = update.effective_user.id
    if user_id in ADMIN_ID:

        if text == 'Главное меню':
            await context.bot.send_message(chat_id=update.effective_chat.id, text='На главную', reply_markup=keyboards.get_admin_base())
            s.set_state(user_id, '0')

        if text == 'Заказы':
            s.set_state(user_id, 'Заказы')
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Заказы:", reply_markup=keyboards.get_admin_orders())

        if text == 'Статистика':
            s.set_state(user_id, 'Статистика')
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Статистика:", reply_markup=keyboards.get_admin_stats())


        if s.get_state(user_id) == "Заказы":
            await vo.get(text, update, context)

        if s.get_state(user_id) == "Статистика":
            await vs.get(text, update, context)

        if s.get_state(user_id) == "Калькулятор":
            await calc.calculate(text, user_id, update, context)

        ### КАЛЬКУЛЯТОР ###
        if text == 'Калькулятор':
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Калькулятор:", reply_markup=keyboards.get_admin_calculate())
            s.set_state(user_id, 'Калькулятор')

        ##Для админов
        if text == "Узнать курс":
           await vc.get(update, context)

        ##Узнать маржу для админов
        if text == "Узнать маржу":
           await vm.get_marge(update, context)

        if s.get_state(user_id) == 'изменить_курс_руб' or s.get_state(user_id) == 'изменить_курс_usdt':
            await vcc.changeCourse(text, s.get_state(user_id), update, context)

        if text == "Изменить курс" or text == "Изменить курс рубля" or text == "Изменить курс usdt":
            await vcc.main(text, update, context)


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
            await vc.get_user(update, context)


        if s.get_state(user_id) == 'ожидание_оценки':

             if text == 'Поставить оценку':
                s.set_state(user_id, 'ожидание_оценки')
                await context.bot.send_message(chat_id=update.effective_chat.id, text='Оцените работу нашего сервиса от 1 до 5 баллов', reply_markup=keyboards.get_user_marks())
                return

        elif s.get_state(user_id) == 'ожидание_оценки':
            # db.set_mark(complete[user_id], text)

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Благодарим за оценку 👍", reply_markup=keyboards.get_user_base())

            s.set_state(user_id, '0')
            return

        if text == "Своя сумма":
            await context.bot.send_message(chat_id=update.effective_chat.id, text=get_message.get_mess("my_sum", False))
            return

        if text == "Поделиться геолокацией":
            geo_handler()
        if text == "Не делиться ⛔️":
            s.set_state(user_id, '0')
            await context.bot.send_message(chat_id=update.effective_chat.id, text=get_message.get_mess("send_geo", False), reply_markup=keyboards.get_user_base())
            return

        ### Для юзеров ###
        if text == "🟰 Выбрать сумму":
            s.set_state(user_id, '0')
            await context.bot.send_message(chat_id=update.effective_chat.id, text=get_message.get_mess("take_sum", False), reply_markup=keyboards.get_user_base())
            return

        ### Для юзеров ###
        ### После выбора суммы ждем когда пользователь выберет способ оплаты ###
        elif (s.get_state(user_id) == 'ожидание_выбора_способа_оплаты'):
            await vu.get(text, update, context)

        elif text.isdigit():

            if s.get_state(user_id) == 'ожидание_оценки':
                s.set_state(user_id, '0')
                # db.set_mark(user_id, text)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=get_message.get_mess("thanks",False), reply_markup=keyboards.get_user_base())
                return



            s.set_state(user_id, 'ожидание_выбора_способа_оплаты')
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

        txt = get_message.get_mess("take_order", False).format(order_id=order_id)

        ## Отправляем сообщение пользователю
        await context.bot.send_message(chat_id=chat_id, text=txt)

        db.update_order(order_id, 'in_progress')

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
        s.set_state(chat_id, 'ожидание_оценки')
        db.update_order(order_id, 'completed')

    if callback_data == 'cancle':

        username, order_id = regexes.admin_apply_user_name(query.message.text)
        chat_id = db.get_chat_id(username)

        for id in ADMIN_ID:
            await context.bot.send_message(chat_id=id, text=f'Заказ {order_id} \nДля @{username} \nОтменен', reply_markup=None)

        await context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=None)

        db.update_order(order_id, 'cancle')


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
            gain_rub = gain_usdt*c.get('rub')

            rub = bat*(c.get('rub')/c_thb)

            username = query.from_user.username
            if query.from_user.username is None:
                username = "--"+query.from_user.first_name+" "+query.from_user.last_name

            db.create_order(ids, username, query.message.chat_id, bat, rub, usdt, course, gain_rub, gain_usdt, trade_method.group(1))

            best_trade_method = commex.get_best(rub)
            txt = get_message.get_mess('order_usdt', True).format(id=ids,
                                                                username=username,
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

            username = query.from_user.username
            if query.from_user.username is None:
                username = "--"+query.from_user.first_name+" "+query.from_user.last_name

            db.create_order(ids, username, query.message.chat_id, bat, rub, usdt, course_rub, gain_rub, gain_usdt, trade_method.group(1))

            txt = get_message.get_mess('order_cash', True).format(id=ids,
                                                                username=username,
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

            username = query.from_user.username
            if query.from_user.username is None:
                if query.from_user.last_name is None:
                    username = "--"+query.from_user.first_name
                else:
                    username = "--"+query.from_user.first_name+" "+query.from_user.last_name


            db.create_order(ids, username, query.message.chat_id, bat, rub, usdt, course, gain_rub, gain_usdt, trade_method.group(1))

            txt = get_message.get_mess('order_bank', True).format(id=ids,
                                                                username=username,
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
async def parse(update, context):
    user_id = update.effective_user.id
    if user_id in ADMIN_ID:

        thread = threading.Thread(target=p.parse_course)
        thread.start()

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Вы не админ")



async def runParser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in ADMIN_ID:
    ##### РАСКОМЕНТИРОВАТЬ
        lock = threading.Lock()

        def run_scheduler():
            # Запуск шедулера каждый час
            schedule.every(1).hour.do(lambda: run_with_lock(p.parse_course, False))

            # Бесконечный цикл для запуска шедулера
            while True:
                schedule.run_pending()
                time.sleep(10)

        def run_with_lock(func, args):
            with lock:
                func(args)

        # Создание и запуск потока для шедулера
        scheduler_thread = threading.Thread(target=run_scheduler)
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

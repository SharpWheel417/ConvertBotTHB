from telegram import Bot, Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
import schedule, time, re, tracemalloc, logging
tracemalloc.start()
import uuid

import convert, commex, db, regexes, geo, keyboards

BOT_TOKEN = '5921193873:AAFtVwAzegmN6G9USoetSEVV7NoSW-BFJRM'
ADMIN_ID = [1194700554, 6920037183]
#I = 1194700554

state = {}
bat = {}
average_rub_user = {}
complete = {}
marje = None
marje = 1.01

user_course_THB = 35.6
user_course_rub = 91.1
admin_course_THB = 35.6
admin_course_rub = 91.1

course_THB = 35.6
course_rub = 91.1


# def parse_course():
    
#     new_course_rub = commex.get_average()
#     global course_rub
#     if (new_course_rub>course_rub):
#             course_rub = new_course_rub
#     print("Average:", course_rub)

#     new_course_THB = bitazza.get_currency()
#     if new_course_THB == 'error':
#         raise Exception('Failed to get THB course from Bitazza')
#     global course_THB
#     if(float(new_course_THB)<course_THB):
#         course_THB = new_course_THB    
#     print(course_THB)
    
#     return float(course_THB)

# parse_course()

# schedule.every(4).hours.do(parse_course)

selected_user_id = None


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def count_rub_clean(bat: int):
    global course_THB
    global course_rub
    global marje
    usdt = bat / course_THB
    rub = (bat / course_THB)*course_rub
    return usdt, rub

def count_rub_marje(bat: int, trade: str):
    global course_THB, marje, course_rub, user_course_rub

    if trade == '💶Наличные':
        course_ruble = user_course_rub
        local_marje = 1.09

    elif trade == '💵Другие банки':
        course_ruble =  user_course_rub
        local_marje = marje
        
    elif trade == '🏧USDT':
        course_ruble = user_course_rub
        local_marje = marje
    else:
        course_ruble = commex.get_by_trade_method(trade, bat, user_course_THB, user_course_rub, marje)
        local_marje = marje

    ## Если мы не смогли найти среднее значение - то ставим обычный средний курс
    if course_ruble == 'error' or course_ruble == 0 or course_ruble is None:
        course_ruble = course_rub

    usdt = (bat / (float(course_THB))*local_marje)
    rub = usdt*course_ruble*marje
    return round(usdt,2), round(rub,2), course_ruble


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

    if not db.check_user_exists(user_id):
        db.add_new_user(user_id, username)

    ### Админ ###
    if user_id in ADMIN_ID:
        #admin panel
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Привет, админ!', reply_markup=keyboards.get_admin_base())

    ### Юзер ###
    else:
        more_button = InlineKeyboardButton('Больше информации', callback_data="more_inf")
        
        reviews_button = InlineKeyboardButton('Прочитать отзывы', url=f"https://t.me/{db.get_review_link()}")
        
        keyboard = InlineKeyboardMarkup([[more_button], [reviews_button]])

        await context.bot.send_message(chat_id=update.effective_chat.id, text=db.get_logo_text(), reply_markup=keyboards.get_user_base())




### Обычное сообщение ####
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global user_course_THB, course_THB, user_course_rub, course_rub
    
    text = update.message.text
    global selected_user_id
    user_id = update.effective_user.id
    if user_id in ADMIN_ID:
        # admin panel
        if text == "Изменить курс рубля":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'ожидание числа для изменения курса рубля'

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения курса рубля (в рублях):", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'ожидание числа для изменения курса рубля':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс для пользователей не изменен, по прежнему РУБ: {user_course_rub} руб.", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                convert.set_course(float(text))
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Курс изменен", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.")
                

        if text == "Изменить курс USDT":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'ожидание числа для изменения курса usdt'
            # Запрашиваем число для изменения курса
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения курса USDT (в USDT):", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'ожидание числа для изменения курса usdt':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс для пользователей не изменен, по прежнему USDT: {user_course_THB} USDT", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                convert.set_course_usdt(float(text))
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Курс изменен", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.")
                
            
        if text == "Изменить процент маржи":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'ожидание числа для изменения маржи'
            # Запрашиваем число для изменения курса
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения процента маржи (в процентах):", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'ожидание числа для изменения маржи':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс не изменен, по прежнему {marje*100} % || {marje}", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                convert.set_marje(float(text))
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Курс изменен", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.Или напишите Отмена.", reply_markup=keyboards.get_admin_base())
                
                
        ##Для админов
        if text == "Узнать курс":
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс с Bitazza USDT/THB  : {course_THB} \n Курс Bitazza для пользователя (без маржи) : {user_course_THB} \nКурс Bitazza для пользователя (с маржой)  : {user_course_THB*marje} \n Курс rub для пользователей: {user_course_rub} \n Процент маржи : {round((marje*100),2)} % || {marje}")
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
            course_THB_RUB = round(((user_course_rub/user_course_THB)*marje),2)

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'''🏷️
Курс THB = {round(user_course_rub/user_course_THB,2)} RUB 🇷🇺
Курс USDT = {user_course_THB} THB 🇹🇭 

Чтобы точнее узнать курс выберите cумму, способ оплаты и нажмите разместить заказ, чтобы связаться с оператором ''', reply_markup=keyboards.get_user_base())
            return
        
        elif user_id in state and state[user_id] == 'ожидание оценки':
            db.set_mark(complete[user_id], text)

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Спасибо за оценку!")
            
            del(state[user_id])

        elif user_id in state and state[user_id] == 'ожидание отзыва':
            db.set_review(complete[user_id], text)

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Спасибо за отзыв!")

            del(state[user_id])
        
        
        if user_id in complete and complete[user_id] is not None:
             
             if text == 'Поставить оценку':
                state[user_id] = 'ожидание оценки'
                await context.bot.send_message(chat_id=update.effective_chat.id, text='Оцените бота от 1 до 5', reply_markup=keyboards.get_user_marks())
                return
             
             if text == 'Оставить отзыв':
                state[user_id] = 'ожидание отзыва'
                await context.bot.send_message(chat_id=update.effective_chat.id, text='Напишиет отзыв на нашу работу', reply_markup=None)
                return
             
        
        if text == "Своя сумма":
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"😄Введите предпочтительную Вам сумму в батах, например, 15756 ⬇️")
            return
        
        if text == "Поделиться геолокацией":
            geo_handler()
        if text == "Не делиться ⛔️":
            del(state[user_id])
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ожидайте ответа оператора ⏱", reply_markup=keyboards.get_user_base())
            return
        
        ### Для юзеров ###
        if text == "Выбрать сумму":
            del(state[user_id])
            
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Теперь вы можете выбрать сумму", reply_markup=keyboards.get_user_base())
            return
        
        ### Для юзеров ###
        ### После выбора суммы ждем когда пользователь выберет способ оплаты ###
        elif user_id in state and state[user_id] == 'ожидание выбора способа оплаты':
            if text in db.get_banks('rus'):
                # Конвертация в баты
                usdt, rub, crub = count_rub_marje(bat[user_id], text)            
                average_rub_user[user_id] = crub
                # Создание кнопки "Запросить"
                request_button = InlineKeyboardButton('Разместить заказ и связаться с оператаром', callback_data="request")
                # Создание клавиатуры с кнопкой "Запросить"
                keyboard = InlineKeyboardMarkup([[request_button]])
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Для получения {bat[user_id]} бат 🇹🇭\nВам необходимо: {rub} руб. ({usdt} USDT) 💰\nРасчет ведется по курсу ({text}) {round(user_course_rub/user_course_THB, 2)} руб. ({user_course_THB} бат за USDT) 📊', reply_markup=keyboard)
                return
            
            
            if text == 'Другая сумма':
                del(state[user_id])
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'😄Введите предпочтительную Вам сумму в батах, например, 15756 ⬇️', reply_markup=keyboards.get_user_base())
                return
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'🪙 Пожалуйста, выберите способ оплаты \nЭто поможет нам выгоднее для Вас рассчитать курс 📊')
                return


        if text.isdigit():

            state[user_id] = 'ожидание выбора способа оплаты'
            bat[user_id] = int(text)

            keyboard = ReplyKeyboardMarkup(keyboards.get_banks(), resize_keyboard=True)

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🪙 Пожалуйста, выберите способ оплаты \nЭто поможет нам выгоднее для Вас рассчитать курс 📊", reply_markup=keyboard)

        else:
            if db.check_request:
                if selected_user_id != None:
                    sel_chat = db.find_chat_id(selected_user_id)
                    if update.effective_chat.id == int(sel_chat):
                        username = db.find_name(update.effective_chat.id)
                        await context.bot.send_message(chat_id=ADMIN_ID[0], text=f'Текст от юзера @{username}: {text}')







## Кнопка "Запросить" ###
async def button_callback(update: Update, context: CallbackContext, *args, **kwargs):

    global admin_course_THB, admin_course_rub
    query = update.callback_query
    # Получаем callback_data из нажатой кнопки
    callback_data = update.callback_query.data

    if callback_data == 'apply':
        ##Меняем кнопки###
        new_inline_keyboard = [[
        InlineKeyboardButton("Выполнен", callback_data='coplete'),
        ]]
    
        reply_markup = InlineKeyboardMarkup(new_inline_keyboard)
        await context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup)

        username, order_id = regexes.admin_apply_user_name(query.message.text)
        chat_id = db.get_chat_id(username)

        ## Отправляем сообщение пользователю
        await context.bot.send_message(chat_id=chat_id, text=f'💬 Ваш заказ взят в работу\nДалее диалог ведет оператор @operator4exchange \nВаш ID заказа: {order_id}')

        db.set_progress(order_id)

    if callback_data == 'coplete':

        username, order_id = regexes.admin_apply_user_name(query.message.text)
        chat_id = db.get_chat_id(username)

        for id in ADMIN_ID:
            await context.bot.send_message(chat_id=id, text=f'Заказ {order_id} \nДля @{username} \nВыполнен!')    

        ## Отправляем сообщение пользователю
        await context.bot.send_message(chat_id=chat_id, text=f'Ваш ID заказа: {order_id} выполнен! \nБлагодарим за сотрудничество и доверие 🤝 \nРасскажите, как прошел Ваш заказ и оставьте отзыв \nТак мы становимся лучше для Вас 💚', reply_markup=keyboards.get_user_complete())

        complete[int(chat_id)] = order_id

        db.set_complete(order_id)


    if callback_data == 'cancel':
        print()

    if callback_data == 'more_inf':
        await context.bot.send_message(chat_id=query.message.chat_id, text=db.get_info_text())

    if callback_data == 'request':

        share_location_button = KeyboardButton("Посмотреть банкоматы и сообщить свое местоположение 🏧", request_location=True)
        select_amount_button = KeyboardButton("Выбрать сумму")
        no_button = KeyboardButton("Не делиться ⛔️")
        keyboard = ReplyKeyboardMarkup([[share_location_button], [no_button], [select_amount_button]], resize_keyboard=True)

        # Отправляем запрос на получение бат
        await context.bot.send_message(chat_id=query.message.chat_id, text="✅ Ваш заказ размещен \n🧑‍💻 Оператор @operator4exchange скоро свяжется с вами \nА пока можете посмотреть, где ближайшие банкомат или просто сообщить курьеру где вы находитесь, отправив свое текущее местоположение 🌎", reply_markup=keyboard)

        ## Парсим из текста запроса пользоавтеля нужные данные
        bat, rub, usdt, rub_thb, thb_usdt, trade_method = regexes.user_request(query.message.text)

        ## Получаем чисту цену
        clean_count = convert.clean(bat, admin_course_THB, admin_course_rub)
        gain = float(rub)-float(clean_count)
        gain_bat = round(gain/ 2)
        gain_usdt = round(gain/admin_course_rub ,2)

        best_course, best_trade = commex.get_best(float(rub))

        ##Создаем ID заказа###
        ids = str(uuid.uuid4())

        if db.check_order_id(ids):
            ids = str(uuid.uuid4())

        mess = f'''
        ID заказа: {ids}
@{query.from_user.username} думает получить {bat} бат через {trade_method}
        
Курс для клиента: {rub_thb} ({thb_usdt} бат/USDT ; {round(rub_thb*thb_usdt, 2)} руб/USDT)
        
Реальный Курс: {round(admin_course_rub/admin_course_THB, 2)} ({admin_course_THB} бат/USDT ; {admin_course_rub} руб/USDT)
        
Сумма оплаты клиентом: {rub} руб. либо {rub*(thb_usdt*rub_thb)} USDT
        
Сумма реальная: {clean_count} руб. ({round(clean_count/admin_course_rub, 2)} USDT)
        
Зарабатываем с этого: {round(gain_bat,2)} бат или {round(gain,2)} руб или {round(gain_usdt, 2)} USDT
        
Bitazza: {admin_course_THB}
        
Самый выгодный способ платежа: {best_trade} {best_course} руб/USDT, {round(best_course/admin_course_THB, 2)} руб/ТНВ'''

        db.request_on(query.message.chat_id)

        cancle_button = InlineKeyboardButton('Отклонить', callback_data="cancle")
        apply_button = InlineKeyboardButton('Взять в работу', callback_data="apply")
        # Создание клавиатуры с кнопкой "Запросить"
        keyboard = InlineKeyboardMarkup([[cancle_button], [apply_button]])


        for chat_id in ADMIN_ID:
            await context.bot.send_message(chat_id=chat_id, text=mess, reply_markup=keyboard)

        
        ### Записываем данные в базу данных ###
        db.create_order(ids, query.from_user.username, float(rub), clean_count, usdt, rub_thb, marje, gain, trade_method)
    
    return True


async def handle_geo(update: Update, context: CallbackContext):
    location = update.message.location
    text = geo.geocoder(location.latitude, location.longitude, update.message.chat_id)
    for chat_id in ADMIN_ID:
        ### Текст с адресом пользователя ###
        await context.bot.send_message(chat_id=chat_id, text=text)
        ### Выводит карту с геопозицией пользователя ####
        await context.bot.send_location(chat_id=chat_id, longitude=location.longitude, latitude=location.latitude)

        
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

    geo_handler = MessageHandler(filters.LOCATION, handle_geo)
    application.add_handler(geo_handler)


    application.run_polling()

while True:
    schedule.run_pending()
    time.sleep(10)

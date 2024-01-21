from telegram import Bot, Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
import schedule, time, re, tracemalloc, logging
tracemalloc.start()

import convert, commex, db, regexes, geo, keyboards


BOT_TOKEN = '5921193873:AAFtVwAzegmN6G9USoetSEVV7NoSW-BFJRM'
ADMIN_ID = [1194700554, 6920037183]
## ГОША 5794240411
## СЕМА 747612773
## X 6920037183


state = {}
bat = {}
average_rub_user = {}
marje = None
marje = 1.1

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

logo_text = 'Добро пожаловать в Обменник USDT to Bat ! \nЗдесь вы можете обменять рубли на тайские баты по выгодному курсу👌 \n✅ Вы отправляете рубли на карту Tinkoff, Сбер или по СБП и получаете баты: \n💳 на тайскую карту \n🛵 курьер привезет вам наличные \n🌴 в Паттайе🏧 в любом ближайшем банкомате Бангкок Банка, Касикорна, Кунгсри🏘 возможна оплата жилья через недоступные в РФ сервисы \nКурс рассчитывается автоматически в режиме реального времени и зависит от суммы обмена. \nПодробнее о процессе вы можете узнать, отправив боту команду /infoВведите сумму в батах, которая вам необходима, или выберете при помощи кнопок: ⬇'

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
    global course_THB, marje, course_rub
    course_ruble = commex.get_by_trade_method(trade, bat, user_course_THB, user_course_rub, marje)

    ## Если мы не смогли найти среднее значение - то ставим обычный средний курс
    if course_ruble == 'error' or course_ruble == 0 or course_ruble is None:
        course_ruble = course_rub

    usdt = bat / (float(course_THB)*marje)
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
            # Создание клавиатуры с кнопкой "Запросить"
        keyboard = InlineKeyboardMarkup([[more_button], [reviews_button]])

        await context.bot.send_message(chat_id=update.effective_chat.id, text=db.get_logo_text(), reply_markup=keyboard,)

        await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите сумму, которая вам необходима в батах или введите ее при помощи кнопок", reply_markup=keyboards.get_user_base())




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

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Курс THB = {course_THB_RUB} RUB \nКурс USDT = {user_course_THB} THB \nЧтобы точнее узнать курс- выберите сумму, способ оплаты')
            return
        
        if text == "Своя сумма":
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Введите предпочтительную Вам сумму в батах, например 15756")
            return
        
        if text == "Поделиться геолокацией":
            geo_handler()
        
        ### Для юзеров ###
        if text == "Выбрать сумму":
            del state[user_id]
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
                request_button = InlineKeyboardButton('Запросить', callback_data="request")
                # Создание клавиатуры с кнопкой "Запросить"
                keyboard = InlineKeyboardMarkup([[request_button]])
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Для получения {bat[user_id]} бат, вам необходимо {rub} руб. ({usdt} USDT)\nРасчёт ведется ({text}) по курсу {course_THB} (USDT: {crub})', reply_markup=keyboard)
                return
            if text == 'Другая сумма':
                del(state[user_id])
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Введите сумму, которая вам необходима в батах или введите ее при помощи кнопок', reply_markup=keyboards.get_user_base())
                return
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Выберите пожалуйста способ оплаты из предложенных нижу', reply_markup=keyboard)
                return


        if text.isdigit():

            state[user_id] = 'ожидание выбора способа оплаты'
            bat[user_id] = int(text)

            keyboard = ReplyKeyboardMarkup(keyboards.get_banks(), resize_keyboard=True)

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Выберите пожалуйста способ оплаты, это поможет нам выгоднее рассчитать курс", reply_markup=keyboard)

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

    if callback_data == 'more_inf':
        await context.bot.send_message(chat_id=query.message.chat_id, text="Курс рассчитывается в автоматическом режиме и зависит от текущего курса на бирже.\nВы можете в течении дня отправлять требуемую сумму в чат и следить за динамикой.\nЗаказ доставки, Общая инструкция по выдачи наличных через банкомат")

    
    if callback_data == 'request':

        share_location_button = KeyboardButton("Поделиться геолокацией", request_location=True)
        select_amount_button = KeyboardButton("Выбрать сумму")
        keyboard = ReplyKeyboardMarkup([[share_location_button], [select_amount_button]], resize_keyboard=True)

        # Отправляем запрос на получение бат
        await context.bot.send_message(chat_id=query.message.chat_id, text="Пожалуйста, ожидайте, оператор с вами свяжется \n А пока можете поделиться своей геолокацей, чтобы нам было легче доставить вам баты", reply_markup=keyboard)

        ## Парсим из текста запроса пользоавтеля нужные данные
        bat, rub, usdt, course, crub = regexes.user_request(query.message.text)

        ## Получаем чисту цену
        clean_count = convert.clean(bat, admin_course_THB, admin_course_rub)
        gain = float(rub)-float(clean_count)
        gain_bat = round(gain/ 2)
        gain_usdt = round(gain/admin_course_rub ,2)

        # mess = f'Пользователь @{query.from_user.username} запросил: \n\nБаты: {bat} \nПользователь заплатит: {rub} руб. \nUSDT: {usdt} \nКурс: {course} \n Зарабатывем с этого: {gain} руб \nЛичный курс пользователя : {average_rub_user[query.message.chat_id]}'

        mess = f'''
        @{query.from_user.username} думает получить {bat} бат через «Сбербанк.... 
        
        Курс для клиента: 2,738 (34,0 бат/USDT ; 91,2 руб/USDT)
        
        Курс для клиента + маржа: 2,813 (34,1 бат/USDT ; 91,7 руб/USDT)Реальный 
        
        курс:2,674 (34,81 бат/USDT ; 91,2 руб/USDT)
        
        Сумма оплаты клиентом: {rub} руб. либо 1 765 USDT
        
        Сумма реальная: {clean_count} руб. (1 724 USDT)
        
        Зарабатываем с этого: {gain_bat} бат или {gain} руб или {gain_usdt} USDT
        
        Bitazza: {admin_course_THB}
        Выбранный способ платежа (): 92,75 руб/USDT, 2,661 руб/ТНВ 
        Самый выгодный способ платежа: Тиньков 92,5 руб/USDT, 2,561 руб/ТНВ 
        Самый выгодный объем для обмена: 100 000 руб тиньк (курс: Тиньк 92,5 руб/USDT, 2,561 руб/THB)'''

        db.request_on(query.message.chat_id)

        for chat_id in ADMIN_ID:
            await context.bot.send_message(chat_id=chat_id, text=mess)
        
        db.create_order(query.from_user.username, float(rub), clean_count, usdt, course, marje, gain)
    
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

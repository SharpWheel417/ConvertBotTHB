from telegram import Bot, Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
import schedule, time, re, tracemalloc, logging
tracemalloc.start()
import uuid

import convert, commex, db, regexes, geo, keyboards, bitazza, calc

BOT_TOKEN = '6472860227:AAEQ3j-L8X9w_fQuSBprXt7PZ_-HyUW_AnU'
#battle-life = 5921193873:AAFtVwAzegmN6G9USoetSEVV7NoSW-BFJRM
#tabletka = 6472860227:AAEQ3j-L8X9w_fQuSBprXt7PZ_-HyUW_AnU
ADMIN_ID = [1194700554, 6920037183]
CHANEL_ID = 'channel4exchange_thai'
#I = 1194700554
# Exchange Admin = 6920037183

state = {}
bat = {}
average_rub_user = {}
complete = {}
marje = None
marje = 1.025
usdt_marje = 1.03
cash_marje = 1.05

# user_course_THB = 100
user_course_THB = 35.6
user_course_rub = 91.1
admin_course_THB = 35.6
admin_course_rub = 91.1

# course_THB = 100
course_THB = 35.6
course_rub = 91.1


def parse_course(update: bool):
    
    new_course_rub = commex.get_average()
    global course_rub, course_THB
    if (new_course_rub>course_rub):
            course_rub = new_course_rub
    print("Average:", course_rub)

    new_course_THB = bitazza.get_currency()
    if new_course_THB == 'error':
        raise Exception('Failed to get THB course from Bitazza')
    global user_course_THB, admin_course_THB
    if update is False:
        if(float(new_course_THB)<course_THB):
            user_course_THB = new_course_THB
        admin_course_THB = new_course_THB
        course_THB = new_course_THB
    else:
        user_course_THB = new_course_THB
        admin_course_THB = new_course_THB
        course_THB = new_course_THB

    print(course_THB)
    
# parse_course(True)

schedule.every(1).hours.do(parse_course)

selected_user_id = None


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def count_thb_usdt_user(bat):
    global user_course_THB, usdt_marje
    return round(float((float(bat)/(float(round(user_course_THB, 2))*(2-usdt_marje)))),2)

def count_rub_marje(bat: int, trade: str, thb_course): 
    global marje, course_rub, user_course_rub, user_course_THB, cash_marje

    if trade == '💵 Наличные':
        course_ruble = user_course_rub
        local_marje = float(cash_marje)

    elif trade == '⚪️ Другие банки':
        course_ruble =  user_course_rub
        local_marje = marje

    elif trade == '🟩 USDT':
        course_ruble = user_course_rub
        local_marje = usdt_marje
    
    else:
        course_ruble = commex.get_by_trade_method(trade, bat, user_course_THB, user_course_rub, marje)
        local_marje = marje

    ## Если мы не смогли найти среднее значение - то ставим обычный средний курс
    if course_ruble == 'error' or course_ruble == 0 or course_ruble is None:
        course_ruble = course_rub

    usdt = (bat / round(user_course_THB*(2-local_marje),2))

    ## Курс Баты к Рублю
    thb_rub = round((course_ruble*local_marje)/(user_course_THB*(2-local_marje)),2)

    cruble = round((course_ruble*local_marje), 2)

    c_rub = round(float(cruble)/round(user_course_THB*(2-local_marje),2),2)
    rub = bat * c_rub
    

    ##курс баты с маржой
    c_thb = round(user_course_THB*(2-local_marje),2)

    # Курс Рубля к Бате

    return round(usdt,2), round(rub,2), cruble, c_rub, c_thb

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

    if user_id in state:
        del(state[user_id])

    if not db.check_user_exists(user_id):
        db.add_new_user(user_id, username)

    ### Админ ###
    if user_id in ADMIN_ID:
        #admin panel
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Привет, админ!', reply_markup=keyboards.get_admin_base())

    ### Юзер ###
    else:
        more_button = InlineKeyboardButton('Больше информации', callback_data="more_inf")
        
        reviews_button = InlineKeyboardButton('Прочитать отзывы', url=f"{db.get_review_link()}")
        
        keyboard = InlineKeyboardMarkup([[more_button], [reviews_button]])

        await context.bot.send_message(chat_id=update.effective_chat.id, text=db.get_logo_text(), reply_markup=keyboard)

        await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите сумму, которая необходима для обмена в батах или выберите при помощи кнопок ⏬", reply_markup=keyboards.get_user_base())



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


        # admin panel
        if text == "Бат в руб":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'бат в руб'

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'бат в руб':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_bath_to_rub(float(text), admin_course_rub, admin_course_THB)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

        if text == "Бат в руб с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'бат в руб с маржой'

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'бат в руб с маржой':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_bath_to_rub_marje(float(text), user_course_rub, user_course_THB, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")



        if text == "Бат в USDT":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'бат в usdt'

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'бат в usdt':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_bath_to_usdt(float(text), admin_course_THB)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

        if text == "Бат в USDT с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'бат в usdt с маржой'

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'бат в usdt с маржой':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_bath_to_usdt_marje(float(text), user_course_THB, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

        if text == "Рубль в бат":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'рубль в бат'

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'рубль в бат':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_rub_to_bat(float(text), admin_course_THB, admin_course_rub)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

        if text == "Рубль в бат с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'рубль в бат с маржой'

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'рубль в бат с маржой':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_rub_to_bat_marje(float(text), user_course_THB, user_course_rub, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

        if text == "Рубль в USDT":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'рубль в usdt'

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'рубль в usdt':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_rub_to_usdt(float(text), admin_course_rub)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")
        

        if text == "Рубль в USDT с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'рубль в usdt с маржой'

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'рубль в usdt с маржой':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_rub_to_usdt_marje(float(text), user_course_rub, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

        if text == "USDT в бат":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'usdt в бат'

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'usdt в бат':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_usdt_to_bat(float(text), admin_course_THB)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

        
        if text == "USDT в бат с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'usdt в бат с маржой'

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'usdt в бат с маржой':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_usdt_to_bat_marje(float(text), user_course_THB, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")


        if text == "USDT в рубль":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'usdt в рубль'

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'usdt в рубль':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_usdt_to_rub(float(text), admin_course_rub)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")


        if text == "USDT в рубль с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'usdt в рубль с маржой'

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif user_id in state and state[user_id] == 'usdt в рубль с маржой':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            
            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_usdt_to_rub_marje(float(text), user_course_rub, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

        





















        ### СТАТИСТИКА ###
        if text == 'Статистика':
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Заказы:", reply_markup=keyboards.get_admin_stats())

        if text == 'Выполненые':

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Вы выполнили: {db.get_ready()} заказов')

        if text == 'Выручка (руб)':
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Выручка: {db.get_revenue()} руб.')

        if text == "Оценки":
        
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Средняя оценка: {db.get_marks()}")

        if text == 'Всего пользователей':

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Всего пользователей: {db.get_count_users()}')
        


        ### ЗАПРОСЫ ###
        if text == 'Запросы':

            orders = db.get_orders_request()

            if orders.__len__()  == 0 or orders is None:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Запросы отсутствуют")

            else:
                for i in orders:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'ID заказа: {i[13]} \nОт {i[12]} \nПользователь: @{i[1]}', reply_markup=keyboards.get_admin_inline_buttons())    


        if text == 'В работе':

            orders = db.get_orders_in_progress()

            if orders.__len__()  == 0 or orders is None:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Заказы в работе отсутствуют")
            else:
                for i in orders:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'ID заказа: {i[13]} \nОт {i[12]} \nПользователь: @{i[1]}', reply_markup=keyboards.get_admin_inline_buttons_in_progress())

        if text == 'Выполненные':

            orders = db.get_orders_complete()

            if orders.__len__()  == 0 or orders is None:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Выполненные заказы отсутствуют")
            else:

                text = ''
                for i in orders:
                    text += f'ID заказа: {i[13]} \nПользователь: @{i[1]} \n\n'

                await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

        if text == 'Отмененные':

            orders = db.get_orders_cancle()

            if orders.__len__()  == 0 or orders is None:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Отмененные заказы отсутствуют")
            else:
                text = 'Отмененные\n'
                for i in orders:
                    text += f'ID заказа: {i[13]} \nПользователь: @{i[1]} \n\n'

                await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        


        ### КУРСЫ ###
        if text == 'Изменить курс':
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите, что хотите изменить:", reply_markup=keyboards.get_admin_courses())

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
                user_course_rub = float(text)
                admin_course_rub = float(text)
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Курс изменен", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.")
                

        if text == "Изменить курс Bitazza":
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
                user_course_THB = float(text)
                admin_course_THB = float(text)
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Курс изменен", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.")
                
            
        

        elif user_id in state and state[user_id] == 'ожидание числа для изменения маржи банков':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс не изменен, по прежнему {marje*100} % || {marje}", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            try:
                marje = float((float(text)/100)+1)
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс маржи для банков изменен на {marje}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]
            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.Или напишите Отмена.", reply_markup=keyboards.get_admin_base())

        elif user_id in state and state[user_id] == 'ожидание числа для изменения маржи для USDT':
            global usdt_marje
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс не изменен, по прежнему {usdt_marje*100} % || {usdt_marje}", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            try:
                usdt_marje = float((float(text)/100)+1)
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс маржи для USDT изменен на {usdt_marje}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]
            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.Или напишите Отмена.", reply_markup=keyboards.get_admin_base())

        elif user_id in state and state[user_id] == 'ожидание числа для изменения маржи для налички':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс не изменен, по прежнему {cash_marje*100} % || {cash_marje}", reply_markup=keyboards.get_admin_base())
                del state[user_id]
                return
            try:
                cash_marje = float((float(text)/100)+1)
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс маржи для налички изменен на {cash_marje}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                del state[user_id]
            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.Или напишите Отмена.", reply_markup=keyboards.get_admin_base())

        if text == "Изменить процент маржи для банков":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'ожидание числа для изменения маржи банков'
            # Запрашиваем число для изменения курса
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения процента маржи для банков (в процентах):", reply_markup=keyboards.get_admin_cancel())

        if text == "Изменить процент маржи для USDT":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'ожидание числа для изменения маржи для USDT'
            # Запрашиваем число для изменения курса
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения процента маржи  для usdt (в процентах):", reply_markup=keyboards.get_admin_cancel())

        if text == "Изменить процент маржи для налички":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'ожидание числа для изменения маржи для налички'
            # Запрашиваем число для изменения курса
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения процента маржи для налички (в процентах):", reply_markup=keyboards.get_admin_cancel())
                
                
        ##Для админов
        if text == "Узнать курс":
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс с Bitazza USDT/THB  : {admin_course_THB} \nКурс Bitazza для пользователя (с маржой)  : {user_course_THB*(2-marje)} \n Курс rub для пользователей (с маржой): {round(user_course_rub*float(marje),2)} \n Процент маржи для банкоа : {round((marje*100),2)} % || {marje} \nПроцент маржи для USDT: {round(float(usdt_marje)*100, 2)} % || {usdt_marje}  \nПроцент маржи Наличка: {round(float(cash_marje)*100, 2)} % || {cash_marje}")
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
            
            course_rub_marje = float(user_course_rub)*float(marje)
            course_thb_marje = float(user_course_THB)*(2-float(marje))

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'''🏷️
Курс THB = {round(float(course_rub_marje)/float(course_thb_marje),2)} RUB 🇷🇺
Курс USDT = {round(float(course_thb_marje), 2)} THB 🇹🇭

Чтобы точнее узнать курс выберите cумму, способ оплаты и нажмите разместить заказ, чтобы связаться с оператором ''', reply_markup=keyboards.get_user_base())
            return
        
        elif user_id in state and state[user_id] == 'ожидание оценки':
            db.set_mark(complete[user_id], text)

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Благодарим за оценку 👍", reply_markup=keyboards.get_user_base())
            
            del(state[user_id])
            return
        
        if user_id in complete and complete[user_id] is not None:
             
             if text == 'Поставить оценку':
                state[user_id] = 'ожидание оценки'
                await context.bot.send_message(chat_id=update.effective_chat.id, text='Оцените работу нашего сервиса от 1 до 5 баллов', reply_markup=keyboards.get_user_marks())
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
        if text == "🟰 Выбрать сумму":
            if user_id in state:
                del(state[user_id])
            
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Теперь вы можете выбрать сумму", reply_markup=keyboards.get_user_base())
            return
        
        ### Для юзеров ###
        ### После выбора суммы ждем когда пользователь выберет способ оплаты ###
        elif user_id in state and state[user_id] == 'ожидание выбора способа оплаты':

            if text in db.get_banks('rus'):
                # Конвертация в баты
                usdt, rub, crub, course_rub, course_THB = count_rub_marje(bat[user_id], text, float(user_course_THB)*(2-float(marje)))            
                if text == '🟩 USDT':
                    usdt = count_thb_usdt_user(bat[user_id])

                average_rub_user[user_id] = crub
                # Создание кнопки "Запросить"
                request_button = InlineKeyboardButton('Разместить заказ и связаться с оператаром', callback_data="request")

                txt = f'Для получения {bat[user_id]} бат 🇹🇭\nВам необходимо: {rub} руб. ({usdt} USDT) 💰\nРасчет ведется по курсу ({text} {round(crub,2)}) {course_rub} руб. ({course_THB} бат за USDT) 📊' 

                if text == '🟩 USDT':
                    txt += "\n*При выборе оплаты в USDT, расчет принимается только в USDT"


                # Создание клавиатуры с кнопкой "Запросить"
                keyboard = InlineKeyboardMarkup([[request_button]])
                await context.bot.send_message(chat_id=update.effective_chat.id, text=txt, reply_markup=keyboard)
                return
            
            
            
            if text == '🟰 Выбрать сумму':
                del(state[user_id])
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'😄Введите предпочтительную Вам сумму в батах, например, 15756 ⬇️', reply_markup=keyboards.get_user_base())
                return
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'🪙 Пожалуйста, выберите способ оплаты \nЭто поможет нам выгоднее для Вас рассчитать курс 📊')
                return


        elif text.isdigit():

            if user_id in state and state[user_id] == 'ожидание оценки':
                del(state[user_id])
                return

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
        await context.bot.send_message(chat_id=chat_id, text=f'💬 Ваш заказ взят в работу\nДалее диалог ведет оператор @operator4exchange \nВаш ID заказа: {order_id}')

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
        await context.bot.send_message(chat_id=chat_id, text=f'Ваш ID заказа: {order_id} выполнен! \nБлагодарим за сотрудничество и доверие 🤝', reply_markup=keyboards.get_user_complete())

        await context.bot.send_message(chat_id=chat_id, text=f'Расскажите, как прошел Ваш заказ и оставьте отзыв \nТак мы становимся лучше для Вас 💚', reply_markup=board)

        complete[int(chat_id)] = order_id

        db.set_complete(order_id)

    if callback_data == 'cancle':

        username, order_id = regexes.admin_apply_user_name(query.message.text)
        chat_id = db.get_chat_id(username)

        for id in ADMIN_ID:
            await context.bot.send_message(chat_id=id, text=f'Заказ {order_id} \nДля @{username} \nОтменен', reply_markup=None)

        await context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=None)   

        db.set_cancle(order_id)

    if callback_data == 'request':

        share_location_button = KeyboardButton("Посмотреть банкоматы и сообщить свое местоположение 🏧", request_location=True)
        select_amount_button = KeyboardButton("🟰 Выбрать сумму")
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

        user_want_usdt = 10

        mess = f'''
        ID заказа: {ids}
@{query.from_user.username} думает получить {bat} бат через {trade_method}
        
Курс для клиента: {rub_thb} ({thb_usdt} бат/USDT ; {round(rub_thb*thb_usdt, 2)} руб/USDT)
        
Реальный Курс: {round(admin_course_rub/admin_course_THB, 2)} ({admin_course_THB} бат/USDT ; {admin_course_rub} руб/USDT)
        
Сумма оплаты клиентом: {rub} руб. либо {round(rub/(thb_usdt*rub_thb), 2)} USDT
        
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
        db.create_order(ids, query.from_user.username, float(rub), clean_count, usdt, rub_thb, marje, gain, trade_method, bat, user_want_usdt)
    
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

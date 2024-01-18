import logging
from telegram import Bot, Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
import tracemalloc
tracemalloc.start()
import schedule
import time


import db
import bitazza
import commex



BOT_TOKEN = '5921193873:AAFtVwAzegmN6G9USoetSEVV7NoSW-BFJRM'
ADMIN_ID = [1194700554]

state = {}
bat = {}
average_rub_user = {}
marje = None
marje = 1.1

user_course_THB = 35.6
user_course_rub = 91.1
course_THB = 35.6
course_rub = 91.1

def set_course(new_course):
    global course
    course = new_course

def set_course_usdt(new_course):
    global course_usdt
    course_usdt = new_course

def set_marje(new_course):
    global marje
    marje = (new_course/100)+1

set_marje(1.1)

def get_average_and_schedule():
    
    new_course_rub = commex.get_average()
    global course_rub
    if (new_course_rub>course_rub):
            course_rub = new_course_rub
    print("Average:", course_rub)

    new_course_THB = bitazza.get_currency()
    if new_course_THB == 'error':
        raise Exception('Failed to get THB course from Bitazza')
    global course_THB
    if(float(new_course_THB)<course_THB):
        course_THB = new_course_THB    
    print(course_THB)
    
    return float(course_THB)

get_average_and_schedule()

schedule.every(4).hours.do(get_average_and_schedule)

logo_text = 'Добро пожаловать в Обменник USDT to Bat ! \nЗдесь вы можете обменять рубли на тайские баты по выгодному курсу👌 \n✅ Вы отправляете рубли на карту Tinkoff, Сбер или по СБП и получаете баты: \n💳 на тайскую карту \n🛵 курьер привезет вам наличные \n🌴 в Паттайе🏧 в любом ближайшем банкомате Бангкок Банка, Касикорна, Кунгсри🏘 возможна оплата жилья через недоступные в РФ сервисы \nКурс рассчитывается автоматически в режиме реального времени и зависит от суммы обмена. \nПодробнее о процессе вы можете узнать, отправив боту команду /infoВведите сумму в батах, которая вам необходима, или выберете при помощи кнопок: ⬇'

selected_user_id = None

db.connect()

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
    course_ruble = commex.get_by_trade_method(trade)

    ## Если мы не смогли найти среднее значение - то ставим обычный средний курс
    if course_ruble == 'error' or course_ruble == 0:
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
        



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username

    if not db.check_user_exists(user_id):
        db.add_new_user(user_id, username)

    if user_id in ADMIN_ID:
        #admin panel
        keyboard = ReplyKeyboardMarkup(
            [['Изменить курс рубля', 'Изменить курс USDT'], ["Изменить процент маржи", 'Узнать курс'], ['Остановить переписку с юзером']],
            resize_keyboard=True
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Привет, админ!', reply_markup=keyboard)


    else:
        keyboard = ReplyKeyboardMarkup(
            [['1000', '2000'], ['3000', '4000'], ['Узнать курс']],
            resize_keyboard=True
        )
        logo_text = db.get_logo_text()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=logo_text, reply_markup=keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    global selected_user_id
    user_id = update.effective_user.id
    if user_id in ADMIN_ID:
        # admin panel
        if text == "Изменить курс рубля":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'ожидание числа для изменения курса рубля'
            # Запрашиваем число для изменения курса
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения курса рубля (в рублях):")

        elif user_id in state and state[user_id] == 'ожидание числа для изменения курса рубля':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс не изменен, по прежнему РУБ: {course} руб.")
                del state[user_id]
                return
            
            try:
                set_course(float(text))
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Курс изменен")
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.")
                

        if text == "Изменить курс USDT":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'ожидание числа для изменения курса usdt'
            # Запрашиваем число для изменения курса
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения курса USDT (в USDT):")

        elif user_id in state and state[user_id] == 'ожидание числа для изменения курса usdt':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс не изменен, по прежнему USDT: {course_usdt} USDT")
                del state[user_id]
                return
            
            try:
                set_course_usdt(float(text))
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Курс изменен")
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.")
                
            
        if text == "Изменить процент маржи":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            state[user_id] = 'ожидание числа для изменения маржи'
            # Запрашиваем число для изменения курса
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения процента маржи (в процентах):")

        elif user_id in state and state[user_id] == 'ожидание числа для изменения маржи':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс не изменен, по прежнему {marje*100} % || {marje}")
                del state[user_id]
                return
            
            try:
                set_marje(float(text))
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Курс изменен")
                # Сбрасываем состояние
                del state[user_id]

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.Или напишите Отмена.")
                
                
        ##Для админов
        if text == "Узнать курс":
            global user_course_THB, course_THB, user_course_rub, course_rub
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс с Bitazza USDT/THB  : {course_THB} \n Курс Bitazza для пользователя (без маржи) : {user_course_THB} \nКурс Bitazza для пользователя (с маржой)  : {user_course_THB*marje} \n Курс с маржой руб: {course*marje} \n Процент маржи : {round((marje*100),2)} % || {marje}")
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
            


    if user_id not in ADMIN_ID:
    
    
        if text == "Узнать курс":
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс USDT : {course_usdt} USDT \nКурс руб : {course_rub} руб.")
            return
        
        if text == "Выбрать сумму":
            keyboard = ReplyKeyboardMarkup(
            [['1000', '2000'], ['3000', '4000'], ['Узнать курс']],
            resize_keyboard=True)

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Теперь вы можете выбрать сумму", reply_markup=keyboard)
            return
        
        elif user_id in state and state[user_id] == 'ожидание выбора способа оплаты':

            del state[user_id]

             # Конвертация в баты
            usdt, rub, crub = count_rub_marje(bat[user_id], text)
            
            average_rub_user[user_id] = crub

            # Создание кнопки "Запросить"
            request_button = InlineKeyboardButton('Запросить', callback_data="request")

            # Создание клавиатуры с кнопкой "Запросить"
            keyboard = InlineKeyboardMarkup([[request_button]])

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Для получения {bat[user_id]} бат, вам необходимо {rub} руб. ({usdt} USDT)\nРасчёт ведется по курсу {course_THB} (USDT: {crub})', reply_markup=keyboard)
            return

        if text.isdigit():

            state[user_id] = 'ожидание выбора способа оплаты'
            bat[user_id] = int(text)

            
            keyboard = ReplyKeyboardMarkup(
                [['Сбербанк', 'Тиькофф', 'Газпром Банк'], [ 'СБП', 'Альфа-банк', 'ВТБ'], ['Промсвязьбанк','Россельхозбанк'], ['МТС-Банк', 'Райффайзен', 'Наличные'], ['Узнать курс', 'Выбрать сумму']],
                resize_keyboard=True
                )



            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Выберите пожалуйста способ оплаты, это поможет нам выгоднее рассчитать курс", reply_markup=keyboard)

        else:
            if db.check_request:
                if selected_user_id != None:
                    sel_chat = db.find_chat_id(selected_user_id)
                    if update.effective_chat.id == int(sel_chat):
                        username = db.find_name(update.effective_chat.id)
                        await context.bot.send_message(chat_id=ADMIN_ID[0], text=f'Текст от юзера @{username}: {text}')





async def button_callback(update: Update, context: CallbackContext, *args, **kwargs):
    query = update.callback_query
    # Получаем callback_data из нажатой кнопки
    callback_data = update.callback_query.data

    # user_id = db.find_chat_id(query.message.chat_id)

    if callback_data == 'request':
        # Отправляем запрос на получение бат
        await context.bot.send_message(chat_id=query.message.chat_id, text="Пожалуйста, ожидайте, оператор с вами свяжется")

        mess = f'Пользователь @{query.from_user.username} запросил: \n\n{query.message.text} \n Личный курс пользователя : {average_rub_user[query.message.chat_id]} '
        db.request_on(query.message.chat_id)
        await context.bot.send_message(chat_id=ADMIN_ID[0], text=mess)
    
    return True


async def handle_geo(update: Update, context: CallbackContext):
    location = update.message.location
    await context.bot.send_message(chat_id=ADMIN_ID, text=f'Latitude: {location.latitude}, Longitude: {location.longitude}')

        
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

    application.add_handler(CallbackQueryHandler(button_callback))


    application.run_polling()

while True:
    schedule.run_pending()
    time.sleep(10)

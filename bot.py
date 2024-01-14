import logging
from telegram import Bot, Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
import tracemalloc
tracemalloc.start()

state = {}

BOT_TOKEN = '5921193873:AAFtVwAzegmN6G9USoetSEVV7NoSW-BFJRM'
ADMIN_ID = [1194700554]

course = 2.17
course_usdt = 33.08
marje = 1.1

selected_user_id = None
selected_chat_id = None

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
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

        await context.bot.send_message(chat_id=update.effective_chat.id, text="Добро пожаловать в Обменник USDT to Bat ! \nЗдесь вы можете обменять рубли на тайские баты по выгодному курсу👌 \n✅ Вы отправляете рубли на карту Tinkoff, Сбер или по СБП и получаете баты: \n💳 на тайскую карту \n🛵 курьер привезет вам наличные \n🌴 в Паттайе🏧 в любом ближайшем банкомате Бангкок Банка, Касикорна, Кунгсри🏘 возможна оплата жилья через недоступные в РФ сервисы \nКурс рассчитывается автоматически в режиме реального времени и зависит от суммы обмена. \nПодробнее о процессе вы можете узнать, отправив боту команду /infoВведите сумму в батах, которая вам необходима, или выберете при помощи кнопок: ⬇", reply_markup=keyboard)

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
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс с Bitazza USDT  : {course_usdt} \nКурс с маржой USDT: {course_usdt*marje} \nКурс руб : {course} руб. \n Курс с маржой руб: {course*marje} \n Процент маржи : {round((marje*100),2)} % || {marje}")
            return
        
        if text == "Остановить переписку с юзером":
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Переиска с юзером {selected_user_id} остановлена")
            selected_user_id = None
            return
        
        
        if selected_user_id:
            await context.bot.get_chat(selected_user_id).send(f'Ответ администратора: {text}')
            
            await context.bot.send_message(chat_id=selected_chat_id, text=f'Ответ администратора: {text}')




    

    if user_id not in ADMIN_ID:
    
        if text == "Узнать курс":
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс USDT : {course_usdt} USDT \nКурс руб : {course} руб.")
            return

        else:
        # Конвертация в баты
            bat = int(text)
            print(bat)
            rub = (bat) * (course)
            usdt = round((bat)/course_usdt, 2)
            print(rub)

            # Создание кнопки "Запросить"
            request_button = InlineKeyboardButton('Запросить', callback_data="request")

            # Создание клавиатуры с кнопкой "Запросить"
            keyboard = InlineKeyboardMarkup([[request_button]])

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Для получения {bat} бат, вам необходимо {rub} руб. ({usdt} USDT)\nРасчёт ведется по курсу {course} (USDT: {course_usdt})', reply_markup=keyboard)

            location_button = KeyboardButton("Отправить местоположение", request_location=True)

            keyboard = ReplyKeyboardMarkup([[location_button]])

            return

def set_course(new_course):
    global course
    course = new_course

def set_course_usdt(new_course):
    global course_usdt
    course_usdt = new_course

def set_marje(new_course):
    global marje
    marje = (new_course/100)+1


async def button_callback(update: Update, context: CallbackContext, *args, **kwargs):
    query = update.callback_query
    # Получаем callback_data из нажатой кнопки
    callback_data = update.callback_query.data

    if callback_data == 'request':
        # Отправляем запрос на получение бат
        await context.bot.send_message(chat_id=query.message.chat_id, text="Пожалуйста, ожидайте, оператор с вами свяжется")

        mess = f'Пользователь @{query.from_user.username} запросил: \n\n{query.message.text}'
        await context.bot.send_message(chat_id=ADMIN_ID, text=mess)
    
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

    message_handler = MessageHandler(filters.TEXT, handle_message)
    application.add_handler(message_handler)

    geo_handler = MessageHandler(filters.LOCATION, handle_geo)
    application.add_handler(geo_handler)

    application.add_handler(CallbackQueryHandler(button_callback))


    application.run_polling()
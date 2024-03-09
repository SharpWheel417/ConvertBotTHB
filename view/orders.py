from telegram import Update
from telegram.ext import ContextTypes
from bot import db, keyboards

async def get(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    if text == 'Запросы':
        orders = db.get_orders_request()
        if orders.__len__()  == 0 or orders is None:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Запросы отсутствуют")
        else:
            for i in orders:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'ID заказа: {i[1]} \nОт {i[12]} \nПользователь: @{i[2]}', reply_markup=keyboards.get_admin_inline_buttons())


    if text == 'В работе':
        orders = db.get_orders_in_progress()
        if orders.__len__()  == 0 or orders is None:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Заказы в работе отсутствуют")
        else:
            for i in orders:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'ID заказа: {i[1]} \nОт {i[12]} \nПользователь: @{i[2]}', reply_markup=keyboards.get_admin_inline_buttons_in_progress())

    if text == 'Выполненные':
        orders = db.get_orders_complete()
        if orders.__len__()  == 0 or orders is None:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Выполненные заказы отсутствуют")
        else:
            messages = []
            message = "Список выполненных звказов:\n"
            for i in orders:
                message += f'ID заказа: {i[1]} \nПользователь: @{i[2]} \n\n'
                if len(message) > 3000:  # Пример максимальной длины сообщения
                    messages.append(message)
                    message = "Список выполненных заказов (продолжение):\n"
            # Добавить последнее сообщение, если оно не пустое
            if message:
                messages.append(message)
            # Отправить сообщения в телеграмм
            for msg in messages:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    if text == 'Отмененные':
        orders = db.get_orders_cancle()
        if orders.__len__()  == 0 or orders is None:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Отмененные заказы отсутствуют")
        else:
            messages = []
            message = "Список отмененных заказов:\n"
            for i in orders:
                message += f'ID заказа: {i[1]} \nПользователь: @{i[2]} \n\n'
                if len(message) > 3000:  # Пример максимальной длины сообщения
                    messages.append(message)
                    message = "Список отмененных заказов (продолжение):\n"
            # Добавить последнее сообщение, если оно не пустое
            if message:
                messages.append(message)
            # Отправить сообщения в телеграмм
            for msg in messages:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
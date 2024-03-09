from telegram import Update
from telegram.ext import ContextTypes
from bot import db, keyboards

async def get(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
        ### СТАТИСТИКА ###

        if text == 'Выполненые':
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Вы выполнили: {db.get_ready()} заказов')

        if text == 'Выручка (руб)':
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Выручка: {db.get_revenue()} руб.')

        if text == "Оценки":

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Средняя оценка: {db.get_marks()}")

        if text == 'Всего пользователей':

            users = db.get_users()
            messages = []
            message = "Список юзеров:\n"
            for row in users:
                name = str(row[1]).replace(' ', '')
                message += f"@{name}\n"
                if len(message) > 3000:  # Пример максимальной длины сообщения
                    messages.append(message)
                    message = "Список юзеров (продолжение):\n"
            # Добавить последнее сообщение, если оно не пустое
            if message:
                messages.append(message)
            # Отправить сообщения в телеграмм
            for msg in messages:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
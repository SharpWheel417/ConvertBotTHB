from telegram import Update
from telegram.ext import ContextTypes
import database.marje as mj


async def change_marje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    parts = text.split()

    if len(parts) >= 4:
        type = parts[1]
        count = float(parts[2])
        marje = float(parts[3])
        try:
            mj.set_marje(type, count, marje)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Курс успешно изменент")
        except Exception as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Произошла ошибка: {e}")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Неверное количество аргумент")



async def get_marge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    marje = mj.get_all()
    messages = []
    message = "Список Маржи:\n"
    for row in marje:
        message += f"Сумма: {row[1]}, Маржа: {row[2]}, Тип: {row[3]}\n"
        if len(message) > 3000:  # Пример максимальной длины сообщения
            messages.append(message)
            message = "Список Маржи (продолжение):\n"
    # Добавить последнее сообщение, если оно не пустое
    if message:
        messages.append(message)
    # Отправить сообщения в телеграмм
    for msg in messages:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
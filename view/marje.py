from telegram import Bot, Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
import schedule, time, re, tracemalloc, logging
tracemalloc.start()
import uuid, threading
from datetime import datetime
import functools
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
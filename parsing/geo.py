import requests

from telegram import Bot, Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext

import database.db as db

GEO_TOKEN = 'pk.2befbac57908662b2b82dd31b3ec964f'

def geocoder(latitude, longitude, chat_id):
    """
    Получаем по координатам текстово местоположение пользователя
    """
    username = db.find_name(chat_id)
    headers = {"Accept-Language": "ru"}
    address = requests.get(f'https://eu1.locationiq.com/v1/reverse.php?key={GEO_TOKEN}&lat={latitude}&lon={longitude}&format=json', headers=headers).json()
    return f'Местоположение @{username} пользователя: {address.get("display_name")}'



async def handle_geo(update: Update, context: CallbackContext, ADMIN_ID):
    location = update.message.location
    text = geocoder(location.latitude, location.longitude, update.message.chat_id)
    for chat_id in ADMIN_ID:
        ### Текст с адресом пользователя ###
        await context.bot.send_message(chat_id=chat_id, text=text)
        ### Выводит карту с геопозицией пользователя ####
        await context.bot.send_location(chat_id=chat_id, longitude=location.longitude, latitude=location.latitude)
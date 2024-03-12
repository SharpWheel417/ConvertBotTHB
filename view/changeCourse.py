from telegram import Update
from telegram.ext import ContextTypes
from bot import db, keyboards
import database.state as s
import database.course as c

async def main(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    if text == "Изменить курс":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите, что хотите изменить:", reply_markup=keyboards.get_admin_courses())


    if text == 'Изменить курс рубля':
        s.set_state(user_id, 'изменить_курс_руб')
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения курса рубля к usdt (в рублях):", reply_markup=keyboards.get_admin_cancel())
    if text == 'Изменить курс usdt':
        s.set_state(user_id, 'изменить_курс_usdt')
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения курса бат к usdt (в бат):", reply_markup=keyboards.get_admin_cancel())

async def changeCourse(text:str, state: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if state == "изменить_курс_руб":
        c.set('rub', float(text))
        s.set_state(user_id, '0')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс рубля изменен на: {c.get('rub')}", reply_markup=keyboards.get_admin_base())


    if state == "изменить_курс_usdt":
        c.set('thb', float(text))
        s.set_state(user_id, '0')
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс usdt изменен на: {c.get('thb')}", reply_markup=keyboards.get_admin_base())
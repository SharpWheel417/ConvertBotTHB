from telegram import Update
from telegram.ext import ContextTypes
import database.get_message as mess
import database.course as c
import database.marje as mj
import database.get_message as get_message
import view.keyboards as kb

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m=mj.get('view', 0)
    thb_marje = c.get('thb')*round((2-m),2)
    rub_marje = c.get('rub')*m
    rub_thb = c.get('rub')/c.get('thb')
    rub_thb_marje = round(rub_marje,2)/round(thb_marje,2)
    txt = mess.get_mess('course', True).format(
        thb = c.get('thb'),
        rub = c.get('rub'),
        thb_marje=round(thb_marje,2),
        rub_marje=round(rub_marje,2),
        rub_thb=round(rub_thb,2),
        rub_thb_marje=round(rub_thb_marje,2)
        )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=txt)



async def get_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thb = c.get('thb')
    rub = c.get('rub')
    m = mj.get_view()
    course_rub_marje = rub * m
    course_thb_marje = thb * (2 - m)
    course_thb_rub = round(course_rub_marje / course_thb_marje, 2)
    course_thb_value = round(course_thb_marje, 2)

    message_text = get_message.get_mess("course", False).format(course_thb_value=course_thb_value, course_thb_rub=course_thb_rub)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text, reply_markup=kb.get_user_base())
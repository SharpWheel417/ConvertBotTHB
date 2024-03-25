from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import database.db as db
import database.course as c
import database.get_message as get_message
import parsing.commex as commex
import database.marje as mj

impor


async def get(text: str, update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if text in db.get_banks('rus'):

        ## Получаем данные из бд
        c_thb = c.get('thb')
        c_rub = c.get('rub')
        u_bat = db.get_bats(user_id)

                # usdt =  u_bat/(2-m)

        if text == '🟩 USDT':
            m = mj.get('usdt', db.get_bats(user_id))
            client_c_thb = round(c_thb*(2-m),2)
            usdt =  u_bat/client_c_thb
            txt = get_message.get_mess("usdt", False).format(usdt=round(usdt,2), course_thb=client_c_thb, bat=u_bat)
            if update.effective_chat.username is None:
                print("\nПользователь ", update.effective_chat.first_name+" "+update.effective_chat.last_name, " запросил ", round(u_bat,2), "USDT: ", round(usdt,2), "Trade: ", text, "\n")

        elif text == '💵 Наличные':
            m = mj.get('cash', db.get_bats(user_id))
            c_m=round(c_thb*(2-m),2)
            r_m = round((c_rub*m),2)
            course = round((r_m/c_m),2)
            rub =  u_bat*course
            usdt =  u_bat/(c_m)
            txt = get_message.get_mess("cash", False).format(course_rub=round(course,2), course_usdt=round(c_m,2), bat=u_bat, rub=round(rub,2), usdt=round(usdt,2))
            print("\nПользователь ", update.effective_chat.username, " запросил ", round(u_bat,2), " USDT: ", round(usdt,2), " Rub: ", rub, " Trade: ", text, "\n")

        else:
            m = mj.get('bank',db.get_bats(user_id))
            rub_course = commex.get_by_trade_method(text, u_bat, c_thb, c_rub, m)
            if rub_course is None:
                rub_course = c.get('rub')

            r_m = float(rub_course)*(m)
            c_m = float(c_thb)*(2-m)

            course_thb_bat = r_m/c_m

            rub =  u_bat*round(course_thb_bat,2)
            usdt =  u_bat/(2-m)
            txt = get_message.get_mess("bank", False).format(course_thb_bat=round(course_thb_bat,2), rub=round(rub,2), bat=u_bat, trade_method=text)
            print("\n ",update.effective_chat.username, " Запросил: ", u_bat, " Ему вывело: ", round(rub,2), " Курс THB: ", c_thb, " Курс RUB: ", c_rub, " Мараж: ", m, " Метод: ", text, "\n")


                # Создание кнопки "Запросить"
        request_button = InlineKeyboardButton('Разместить заказ', callback_data="request")


                # Создание клавиатуры с кнопкой "Запросить"
        keyboard = InlineKeyboardMarkup([[request_button]])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=txt, reply_markup=keyboard)
        return

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=get_message.get_mess("please", False))
        return
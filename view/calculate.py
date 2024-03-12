from telegram import Update
from telegram.ext import ContextTypes
import database.state as s
import view.keyboards as keyboards
import model.calc as calc

# admin panel
async def calculate(text: str, user_id: int, update: Update, context: ContextTypes.DEFAULT_TYPE):

    if text == "Бат в руб":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            s.set_state_calc(user_id, 'бат_в_руб')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

    elif s.get_state_calc(user_id) == 'бат_в_руб':
        if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                s.set_state_calc(user_id, '0')
                return

        try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_bath_to_rub(float(text))}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                s.set_state_calc(user_id, '0')

        except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

    if text == "Бат в руб с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            s.set_state_calc(user_id, 'бат_в_руб_с_маржой')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число и маржу (1000 1.02)", reply_markup=keyboards.get_admin_cancel())

    elif s.get_state_calc(user_id) == 'бат_в_руб_с_маржой':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                s.set_state_calc(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                count, marje = (float(x) for x in text.split(' '))
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_bath_to_rub_marje(count, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                s.set_state_calc(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")



    if text == "Бат в USDT":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            s.set_state_calc(user_id, 'бат_в_usdt')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

    elif s.get_state_calc(user_id) == 'бат_в_usdt':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                s.set_state_calc(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_bath_to_usdt(float(text))}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                s.set_state_calc(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

    if text == "Бат в USDT с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            s.set_state_calc(user_id, 'бат_в_usdt_с_маржой')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число и маржу (1000 1.02)", reply_markup=keyboards.get_admin_cancel())

    elif s.get_state_calc(user_id) == 'бат_в_usdt_с_маржой':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                s.set_state_calc(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                count, marje = (float(x) for x in text.split(' '))
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_bath_to_usdt_marje(count, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                s.set_state_calc(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректно. Введите число и маржу (1000 1.02)")

    if text == "Рубль в бат":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            s.set_state_calc(user_id, 'рубль_в_бат')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

    elif s.get_state_calc(user_id) == 'рубль_в_бат':
        if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                s.set_state_calc(user_id, '0')
                return

        try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_rub_to_bat(float(text))}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                s.set_state_calc(user_id, '0')

        except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

    if text == "Рубль в бат с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            s.set_state_calc(user_id, 'рубль_в_бат_с_маржой')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число и маржу (1000 1.02)", reply_markup=keyboards.get_admin_cancel())

    elif s.get_state_calc(user_id) == 'рубль_в_бат_с_маржой':
        if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                s.set_state_calc(user_id, '0')
                return

        try:
                # Выполняем действия для изменения курса
                count, marje = (float(x) for x in text.split(' '))
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_rub_to_bat_marje(count, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                s.set_state_calc(user_id, '0')

        except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректно. Введите число и маржу (1000 1.02)")

    if text == "Рубль в USDT":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            s.set_state_calc(user_id, 'рубль_в_usdt')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

    elif s.get_state_calc(user_id) == 'рубль_в_usdt':
        if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                s.set_state_calc(user_id, '0')
                return

        try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_rub_to_usdt(float(text))}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                s.set_state_calc(user_id, '0')

        except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")


    if text == "Рубль в USDT с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            s.set_state_calc(user_id, 'рубль_в_usdt_с_маржой')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число и маржу (1000 1.02) ", reply_markup=keyboards.get_admin_cancel())

    elif s.get_state_calc(user_id) == 'рубль_в_usdt_с_маржой':
        if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                s.set_state_calc(user_id, '0')
                return

        try:
                # Выполняем действия для изменения курса
                count, marje = (float(x) for x in text.split(' '))
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_rub_to_usdt_marje(count, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                s.set_state_calc(user_id, '0')

        except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректно Введите число и маржу (1000 1.02)")

    if text == "USDT в бат":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            s.set_state_calc(user_id, 'usdt_в_бат')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

    elif s.get_state_calc(user_id) == 'usdt_в_бат':
        if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                s.set_state_calc(user_id, '0')
                return

        try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_usdt_to_bat(float(text))}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                s.set_state_calc(user_id, '0')

        except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")


    if text == "USDT в бат с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            s.set_state_calc(user_id, 'usdt_в_бат_с_маржой')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число и маржу (1000 1.02)", reply_markup=keyboards.get_admin_cancel())

    elif s.get_state_calc(user_id) == 'usdt_в_бат_с_маржой':
        if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                s.set_state_calc(user_id, '0')
                return

        try:
                # Выполняем действия для изменения курса
                count, marje = (float(x) for x in text.split(' '))
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_usdt_to_bat_marje(count, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                s.set_state_calc(user_id, '0')

        except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректно Введите число и маржу (1000 1.02)")


    if text == "USDT в рубль":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            s.set_state_calc(user_id, 'usdt_в_рубль')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

    elif s.get_state_calc(user_id) == 'usdt_в_рубль':
        if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                s.set_state_calc(user_id, '0')
                return

        try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_usdt_to_rub(float(text))}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                s.set_state_calc(user_id, '0')

        except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")


    if text == "USDT в рубль с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            s.set_state_calc(user_id, 'usdt_в_рубль_с_маржой')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число и маржу (1000 1.02)", reply_markup=keyboards.get_admin_cancel())

    elif s.get_state_calc(user_id) == 'usdt_в_рубль_с_маржой':
        if text == "Отмена":
                # Сбрасываем состояние

                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                s.set_state_calc(user_id, '0')
                return

        try:
                # Выполняем действия для изменения курса
                count, marje = (float(x) for x in text.split(' '))
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_usdt_to_rub_marje(count, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                s.set_state_calc(user_id, '0')

        except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректно Введите число и маржу (1000 1.02)")
# admin panel
        if text == "Бат в руб":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'бат в руб')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif db.get_state(user_id) == 'бат в руб':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_bath_to_rub(float(text), admin_course_rub, admin_course_THB)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

        if text == "Бат в руб с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'бат в руб с маржой')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif db.get_state(user_id) == 'бат в руб с маржой':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_bath_to_rub_marje(float(text), user_course_rub, user_course_THB, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")



        if text == "Бат в USDT":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'бат в usdt')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif db.get_state(user_id) == 'бат в usdt':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_bath_to_usdt(float(text), admin_course_THB)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

        if text == "Бат в USDT с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'бат в usdt с маржой')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif db.get_state(user_id) == 'бат в usdt с маржой':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_bath_to_usdt_marje(float(text), user_course_THB, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

        if text == "Рубль в бат":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'рубль в бат')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif db.get_state(user_id) == 'рубль в бат':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_rub_to_bat(float(text), admin_course_THB, admin_course_rub)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

        if text == "Рубль в бат с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'рубль в бат с маржой')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif db.get_state(user_id) == 'рубль в бат с маржой':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_rub_to_bat_marje(float(text), user_course_THB, user_course_rub, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

        if text == "Рубль в USDT":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'рубль в usdt')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif db.set_state(user_id) == 'рубль в usdt':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_rub_to_usdt(float(text), admin_course_rub)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")


        if text == "Рубль в USDT с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'рубль в usdt с маржой')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif db.get_state(user_id) == 'рубль в usdt с маржой':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_rub_to_usdt_marje(float(text), user_course_rub, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")

        if text == "USDT в бат":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'usdt в бат')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif db.get_state(user_id) == 'usdt в бат':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_usdt_to_bat(float(text), admin_course_THB)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")


        if text == "USDT в бат с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'usdt в бат с маржой')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif db.get_state(user_id) == 'usdt в бат с маржой':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_usdt_to_bat_marje(float(text), user_course_THB, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")


        if text == "USDT в рубль":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'usdt в рубль')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif db.get_state(user_id) == 'usdt в рубль':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_usdt_to_rub(float(text), admin_course_rub)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")


        if text == "USDT в рубль с маржой":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'usdt в рубль с маржой')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число", reply_markup=keyboards.get_admin_cancel())

        elif db.get_state(user_id) == 'usdt в рубль с маржой':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отмена", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return

            try:
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{calc.get_usdt_to_rub_marje(float(text), user_course_rub, marje)}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число.")
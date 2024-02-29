
        ### КУРСЫ ###
        if text == 'Изменить курс':
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите, что хотите изменить:", reply_markup=keyboards.get_admin_courses())

        # admin panel
        if text == "Изменить курс рубля":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'ожидание числа для изменения курса рубля')

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения курса рубля (в рублях):", reply_markup=keyboards.get_admin_cancel())

        elif db.get_state(user_id) == 'ожидание числа для изменения курса рубля':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс для пользователей не изменен, по прежнему РУБ: {user_course_rub} руб.", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return

            try:
                user_course_rub = float(text)
                admin_course_rub = float(text)
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Курс изменен", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.")


        if text == "Изменить курс Bitazza":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'ожидание числа для изменения курса usdt')
            # Запрашиваем число для изменения курса
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения курса USDT (в USDT):", reply_markup=keyboards.get_admin_cancel())

        elif db.get_state(user_id) == 'ожидание числа для изменения курса usdt':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс для пользователей не изменен, по прежнему USDT: {user_course_THB} USDT", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return

            try:
                user_course_THB = float(text)
                admin_course_THB = float(text)
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Курс изменен", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')

            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.")




        elif db.get_state(user_id) == 'ожидание числа для изменения маржи банков':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс не изменен, по прежнему {marje*100} % || {marje}", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return
            try:
                marje = float((float(text)/100)+1)
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс маржи для банков изменен на {marje}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')
            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.Или напишите Отмена.", reply_markup=keyboards.get_admin_base())

        elif db.get_state(user_id) == 'ожидание числа для изменения маржи для USDT':
            global usdt_marje
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс не изменен, по прежнему {usdt_marje*100} % || {usdt_marje}", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return
            try:
                usdt_marje = float((float(text)/100)+1)
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс маржи для USDT изменен на {usdt_marje}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')
            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.Или напишите Отмена.", reply_markup=keyboards.get_admin_base())

        elif db.get_state(user_id) == 'ожидание числа для изменения маржи для налички':
            if text == "Отмена":
                # Сбрасываем состояние
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс не изменен, по прежнему {cash_marje*100} % || {cash_marje}", reply_markup=keyboards.get_admin_base())
                db.set_state(user_id, '0')
                return
            try:
                cash_marje = float((float(text)/100)+1)
                # Выполняем действия для изменения курса
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Курс маржи для налички изменен на {cash_marje}", reply_markup=keyboards.get_admin_base())
                # Сбрасываем состояние
                db.set_state(user_id, '0')
            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Некорректное число. Введите число для изменения курса.Или напишите Отмена.", reply_markup=keyboards.get_admin_base())

        if text == "Изменить процент маржи для банков":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'ожидание числа для изменения маржи банков')
            # Запрашиваем число для изменения курса
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения процента маржи для банков (в процентах):", reply_markup=keyboards.get_admin_cancel())

        if text == "Изменить процент маржи для USDT":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.set_state(user_id, 'ожидание числа для изменения маржи для USDT')
            # Запрашиваем число для изменения курса
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения процента маржи  для usdt (в процентах):", reply_markup=keyboards.get_admin_cancel())

        if text == "Изменить процент маржи для налички":
            # Устанавливаем состояние в 'ожидание числа для изменения курса'
            db.get_state(user_id, 'ожидание числа для изменения маржи для налички')
            # Запрашиваем число для изменения курса
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите число для изменения процента маржи для налички (в процентах):", reply_markup=keyboards.get_admin_cancel())
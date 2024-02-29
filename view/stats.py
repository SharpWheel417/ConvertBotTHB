
        ### СТАТИСТИКА ###
        if text == 'Статистика':
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Заказы:", reply_markup=keyboards.get_admin_stats())

        if text == 'Выполненые':

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Вы выполнили: {db.get_ready()} заказов')

        if text == 'Выручка (руб)':
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Выручка: {db.get_revenue()} руб.')

        if text == "Оценки":

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Средняя оценка: {db.get_marks()}")

        if text == 'Всего пользователей':

            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Всего пользователей: {db.get_count_users()}')
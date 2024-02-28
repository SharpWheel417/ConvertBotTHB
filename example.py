def order_text(bat, trade_method, course_thb, course_rub, rub, usdt):

    if (trade_method == '💵 Наличные'):
        mess = f'''
        Курс USD {course_thb}$📊

Курс RUB {course_rub}₽📊

Для получения {bat} бат 🇹🇭
Вам необходимо: {rub} руб. или {usdt} USD 💰

Расчет ведется по курсу {trade_method}
    '''
    elif(trade_method == '🟩 USDT'):
        mess = f'''
        Курс {course_thb} 📊

Для получения {bat} бат 🇹🇭
Вам необходимо:
{round(float(bat)/float(course_thb), 2)} USDT 💰

Расчет ведется по курсу
🟩 USDT

*При выборе оплаты в USDT, расчет принимается только в USDT
'''
    else:
        mess = f'''
        Курс {round(float(course_rub),2)}📊

Для получения {bat} бат 🇹🇭
Вам необходимо: {rub} руб.

Расчет ведется по курсу
{trade_method}
'''


    return mess
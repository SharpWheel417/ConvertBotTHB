
import requests


class Payment:
    def __init__(self, responce):
        for key, value in responce.items():
            setattr(self, key, value)


def get(page: int):
    url = "https://www.commex.com/bapi/c2c/v1/friendly/c2c/ad/search"
    if not isinstance(page, int):
        raise ValueError("Page должен быть целым числом")
    data = {"page": page, "asset": "USDT",
            "fiat": "RUB", "tradeType": "BUY", "rows": 10}
    response = requests.post(url, json=data)
    response = response.json()
    # print(response)
    if not 'data' in response:
        raise ValueError("Нет данных")
    for data in response['data']:
        yield Payment(data['adDetailResp'])

banks = ['Raiffeisenbank', 'SBP - Fast Bank Transfer', 'Sberbank', 'Tinkoff', 'Alfa-bank', 'VTB Bank', 'Promsvyaz bank', 'Sovkombank', 'Rosselkhozbank', 'Gazprombank', 'MTS-Bank']


trade_method = {
    'Сбербанк':'Sberbank',
    'Тиькофф':'Tinkoff',
    'Газпром Банк':'Gazprombank',
    'СБП':'SBP - Fast Bank Transfer',
    'Альфа-банк':'Alfa-bank',
    'ВТБ':'VTB Bank',
    'Промсвязьбанк':'Promsvyaz bank',
    'Россельхозбанк':'Rosselkhozbank',
    'МТС-Банк':'MTS-Bank',
    'Райффайзен':'Raiffeisenbank',
    'Наличные':'',
    }

def get_get():
    for i in range(1, 10000):
        try:
            for j in get(i):
                yield j
        except ValueError:
            break
        except Exception as e:
            print(f'Остановка по причине: {e}')
            break


def get_by_trade_method(method):
    x=0
    sum = 0
    average = 0
    tr = trade_method[method]
    for i in get_get():
        if tr in list(map(lambda x: x['tradeMethodName'], i.tradeMethods)):
            if x<5:
                x+=1
                sum += float(i.price)
            else:
                average = sum/x
                print(average)
                return round(average,2)
    if x>0:
        average = sum/x
        print(average)
        return round(average,2)      
        


def get_average():
    x=0
    sum = 0
    average = 0
    for i in get_get():
        mapped_methods = list(map(lambda x: x['tradeMethodName'], i.tradeMethods))
                    
        if x<10:
            if mapped_methods[0] in banks:
                x+=1
                sum += float(i.price)
        else:
            average = sum/x
            print(average)
            return round(average,2)
        # print(
        #     'Price:', i.price,
        #     'TradeMethods:', *map(lambda x: x['tradeMethodName'], i.tradeMethods),
        #     'ID:', i.adNo,
        #     'TradeType', i.tradeType,
        #     # 'completedOrderNum', i.CompletedOrderNum,
        #     'minSingleTransAmount', i.minSingleTransAmount,
        #     'maxSingleTransAmount', i.maxSingleTransAmount,
        # )

# print(get_average())
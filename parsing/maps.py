import googlemaps

# Создание экземпляра клиента Google Maps с использованием вашего API-ключа
api_gmaps_key = "YOUR_API_KEY"
map_client = googlemaps.Client(api_gmaps_key)

# Функция для получения адресов ближайших банкоматов
def get_nearest_atm_addresses(latitude, longitude):
    # Вызов Google Maps API для поиска ближайших банкоматов
    result = map_client.places_nearby(
        location=(latitude, longitude),
        radius=10000,  # Радиус поиска банкоматов (в метрах)
        type='Bualuang ATM'  # Тип объекта (банкомат)
    )
    
    # Извлечение адресов банкоматов из результатов API
    addresses = []
    for place in result['results']:
        address = place['vicinity']
        addresses.append(address)
    
    return addresses

# Получение координат от пользователя
latitude = ...
longitude = ...

# Получение адресов ближайших банкоматов
atm_addresses = get_nearest_atm_addresses(latitude, longitude)

# Отправка адресов банкоматов пользователю
for address in atm_addresses:
    # Отправка адреса пользователю (например, через Telegram API)
    send_message_to_user(address)
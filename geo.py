import requests
import database.db as db

GEO_TOKEN = 'pk.2befbac57908662b2b82dd31b3ec964f'

def geocoder(latitude, longitude, chat_id):
    """
    Получаем по координатам текстово местоположение пользователя
    """
    username = db.find_name(chat_id)
    headers = {"Accept-Language": "ru"}
    address = requests.get(f'https://eu1.locationiq.com/v1/reverse.php?key={GEO_TOKEN}&lat={latitude}&lon={longitude}&format=json', headers=headers).json()
    return f'Местоположение @{username} пользователя: {address.get("display_name")}'
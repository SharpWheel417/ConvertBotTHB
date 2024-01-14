from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Установите путь к исполняемому файлу Chrome WebDriver
webdriver_path = './chromedriver_mac64/'

# Создаем экземпляр WebDriver с использованием Chrome
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Запуск в режиме "без графического интерфейса"
driver = webdriver.Chrome(options=chrome_options)

# Открываем страницу с курсом доллара к батам
url = 'https://trade.bitazza.com/th/exchange'
driver.get(url)

# Дождитесь загрузки страницы (может потребоваться настройка времени ожидания)
# Пример:
driver.implicitly_wait(10)  # Ожидание в течение 10 секунд

# Найдите и извлеките курс доллара к батам
# На основе структуры HTML-кода страницы bitazza.com
# вам нужно найти соответствующий элемент и извлечь нужную информацию

# Пример:
element = driver.find_element(By.CLASS_NAME, 'instrument-selector__trigger')
element.click()



driver.implicitly_wait(10)

# Обработка данных о курсе доллара к батам
# вам может потребоваться дополнительная обработка
# для получения именно числового значения курса

# Пример:
# rate = rate.replace('THB', '').strip()
# rate = float(rate)

# Вывод курса доллара к батам
# print(f"Курс доллара к батам: {rate}")

# Закрываем браузер после использования
driver.quit()
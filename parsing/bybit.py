from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time

def get_currency() -> str:

    """
    Функция получает текущую валюту на веб-странице.
    :return: текущая валюта в виде строки, либо 'error' в случае ошибки
    """

    try:
        # Создаем экземпляр WebDriver с использованием Chrome
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')

        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Safari/605.1.15"
        chrome_options.add_argument(f"user-agent={user_agent}")

        driver = webdriver.Chrome(options=chrome_options)

        # Открываем страницу с курсом доллара к батам
        url = 'https://www.bybit.com/en/convert/thb-to-usdt/'
        driver.get(url)

        print(driver.title)

        time.sleep(5)


        course = driver.execute_script(
    """return document.querySelector('.card-info-price').textContent;""")

        driver.quit()
        return course

    except WebDriverException as e:
        print(f"An error occurred: {e}")
        return 'error'


def get_currency_rub() -> str:

    """
    Функция получает текущую валюту на веб-странице.
    :return: текущая валюта в виде строки, либо 'error' в случае ошибки
    """

    try:
        # Создаем экземпляр WebDriver с использованием Chrome
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')

        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Safari/605.1.15"
        chrome_options.add_argument(f"user-agent={user_agent}")

        driver = webdriver.Chrome(options=chrome_options)

        # Открываем страницу с курсом доллара к батам
        url = 'https://www.bybit.com/en/convert/rub-to-usdt/'
        driver.get(url)

        print(driver.title)

        time.sleep(5)


        course = driver.execute_script(
    """return document.querySelector('.card-info-price').textContent;""")

        driver.quit()
        return course

    except WebDriverException as e:
        print(f"An error occurred: {e}")
        return 'error'

print(get_currency_rub())

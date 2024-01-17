from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_currency() -> str:
    # Установите путь к исполняемому файлу Chrome WebDriver
    webdriver_path = './chromedriver_mac64/'

    # Создаем экземпляр WebDriver с использованием Chrome
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Запуск в режиме "без графического интерфейса"
    driver = webdriver.Chrome(options=chrome_options)

    # Открываем страницу с курсом доллара к батам
    url = 'https://trade.bitazza.com/th/exchange'
    driver.get(url)
    
    """
    Функция получает текущую валюту на веб-странице.

    :param driver: экземпляр веб-драйвера
    :return: текущая валюта в виде строки, либо 'error' в случае ошибки
    """
    elementCords = driver.execute_script(
        """return (()=>{let b = null;while(b === null){b=document.querySelector('div.instrument-selector-popover__popover > button')}b.click();for (let i of document.querySelectorAll('img[alt="product icon"]')){if(i.parentElement.textContent==='USDT/THB'){return i.parentElement.parentElement.parentElement}}})();""")
    elementCords.click()
    
    for _ in range(100):
        value = driver.execute_script("""return document.title""")
        value = value.split('|')
        if len(value) > 1 and value[1].strip() == 'USDT/THB':
            return value[0].strip()
            driver.quit()
        driver.implicitly_wait(1)
    return 'error'

print(get_currency())


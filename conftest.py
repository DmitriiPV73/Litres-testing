import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
# import logging

@pytest.fixture(scope="function")
def browser():
    """
    Фикстура для инициализации браузера Chrome
    """
    chrome_options = Options()

    # Настройки для Litres.ru
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--lang=ru")

    # Для обхода блокировок
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)

    # Установка неявного ожидания
    driver.implicitly_wait(10)

    # Настройка логирования
    # logging.basicConfig(level=logging.INFO)
    # driver.logger = logging.getLogger(__name__)

    yield driver

    driver.quit()


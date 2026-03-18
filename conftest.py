import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
import time

""" Добавляем опции командной строки для выбора браузера"""
def pytest_addoption(parser):
    parser.addoption(
        "--browser", # Название опции в командной строке
        action="store", # Сохраняем значение, переданное пользователем
        default="chrome", # Значение по умолчанию, если опция не указана
        help="Выбор браузера: Chrome or Firefox", # Справка для пользователя
    )
    """ Добавляем опции для возможности выбора отображения браузера"""
    parser.addoption(
        "--headless", # Опция, когда браузер не отображает графический интерфейс (не отрисовывает на экране)
        action="store_true", # Устанавливает True, если флаг указан
        default=False, # По умолчанию False - браузер видимый
        help="Запуск в headless режиме (без GUI)" # Справка для пользователя
    )

"""Основная фикстура. Создает и настраивает WebDriver для каждого теста"""
@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    # driver = None

    if browser.lower() == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new") # Настройка режима без отображения (headless)
            options.add_argument("--window-size=1920x1080") # Устоановка размера окна
            options.add_argument("--disable-notifications") # Отключение уведомлений
            options.add_argument("--disable-popup-posting") # Отключение встроенного блокировщика всплывающих окон
            options.add_argument("--disable-blink-features=AutomationControlled") # Отключает свойства в движке Blink, что бы убрать признаки автоматизации
            options.add_experimental_option("excludeSwitches", ["enable-automation"]) # Маскировка автоматизации (чтобы сайт не определил управление роботом)
            options.add_experimental_option('useAutomationExtension', False) # Отключает использование расширения автоматизации Chrome

        service = ChromeService(ChromeDriverManager().install()) # Автоматическая загрузка и установка драйвера через ChromeDriverManager
        driver = webdriver.Chrome(service=service, options=options) # Создается веб-драйвер для управления Chrome в автоматическом режиме

    elif browser.lower() == "firefox":
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920x1080")

        service = СркщьуService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    """Общие настройки и завершение"""
    driver.implicitly_wait(10) # Неявное ожидание
    driver.maximize_window() # Максимизируем окно
    # vield driver # Возвращаем драйвер для использования в тестах
    time.sleep(2) # Пауза в 2 с
    driver.quit() # Закрываем браузер и освобождаем ресурсы

"""Фикстура базового URL для каждого теста"""
@pytest.fixture(scope="function")
def base_url(): # Простая фикстура без параметров
    return "https://www.avito.ru/" # Возвращает строку с адресом сайта

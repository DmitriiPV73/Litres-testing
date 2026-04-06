import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException
)
from pages.base_page import BasePage

class MainPage(BasePage):
    """Главная страница"""
    # Поле поиска
    SEARCH_MAIN_INPUT = (By.XPATH, '//*[@id="layout-root"]/header/div[2]/div[2]/div[2]/div/form/div/input')
    # Кнопка "Найти"
    SEARCH_MAIN_BUTTON = (By.XPATH, '//*[@id="layout-root"]/header/div[2]/div[2]/div[2]/div/form/div/button')
    # Кнопка "Популярное"
    POPULAR_TAB = (By.XPATH, '//*[@id="lowerMenuWrap"]/nav/div/a[4]')
    # Кнопка cookie
    COOKIE_ACCEPT_BUTTON = (By.CSS_SELECTOR, '#__next > div._415eb400.b0cbc1ce > button > div')
    # Заголовок на странице "Популярное" для проверки перехода
    PAGE_HEADING = (By.XPATH, '//h1/span[text()="Лучшие книги"]')

    def open(self):
        """Открытие главной страницы"""
        with allure.step("Открыть главную страницу Litres.ru"):
            self.open_url("https://www.litres.ru/")
            self.accept_cookies()
        return self

    def accept_cookies(self):
        """Принять куки, если они есть"""
        with allure.step("Принять cookie"):
            try:
                self.click_element(self.COOKIE_ACCEPT_BUTTON)
                return True
            except TimeoutException:
                return False  # Куки нет или уже приняты

    def go_to_tab(self):
        """Переход на вкладку по индикатору"""
        with allure.step("Перейти на вкладку 'Популярное'"):
            try:
                self.click_element(self.POPULAR_TAB)
            except Exception:
                raise

    def is_popular_page_loaded(self):
        """Проверка, что страница 'Популярное' загрузилась"""
        with allure.step("Проверить заголовок страницы"):
            # Используем метод из BasePage
            return self.is_element_displayed(self.PAGE_HEADING)
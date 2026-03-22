from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class JobPage(BasePage):
    # Локаторы на странице "Работа"
    PAGE_TITLE = (By.TAG_NAME, "h1")
    SEARCH_VACANCY_INPUT = (By.XPATH, "//input[@placeholder='Должность']")

    def __init__(self, driver, url="https://www.avito.ru/perm/rabota"):
        BasePage.__init__(self, driver, url)

    def is_loaded(self):
        """Проверка, что страница загрузилась"""
        try:
            self.driver.find_element(*self.PAGE_TITLE)
            return True
        except:
            return False

    def get_page_title(self):
        """Получить заголовок страницы"""
        element = self.driver.find_element(*self.PAGE_TITLE)
        return element.text

    def search_vacancy(self, keyword: str):
        """Ввести запрос в поле поиска вакансий"""
        search_input = self.driver.find_element(*self.SEARCH_VACANCY_INPUT)
        search_input.clear()  # Очистить поле, если там есть текст
        search_input.send_keys(keyword)
        search_input.submit()  # Отправить форму (нажатие Enter)
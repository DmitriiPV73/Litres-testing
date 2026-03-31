import time
from selenium.common.exceptions import ElementClickInterceptedException

import allure
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class SearchResultsPage(BasePage):
    """Страница результатов поиска"""
    # Поле поиска
    SEARCH_INPUT = (By.CSS_SELECTOR, '#layout-root > header > div._5d332c5b > div._2834e32d > div.cc56edc5 > div > form > div > input')
    # Кнопка "Найти"
    SEARCH_BUTTON = (By.XPATH, '//*[@id="layout-root"]/header/div[2]/div[2]/div[2]/div/form/div/button')
    # Заголовок книги (первой)
    BOOK_TITLES = (By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/a[1]')
    # Заголовки книг
    BOOK_TITLES_ALL = (By.XPATH, '//a[@data-testid="art__title"]')
    # Кнопка выбора "Бизнес-книги"
    BUSINESS_BOOKS_BUTTON = (By.XPATH, '//*[@id="main"]/div[2]/div/div[1]/div[1]/div[2]/div/div[4]/a')
    # Поле чек-бокса "Текст"
    CHECK_BOX_TEXT = (By.XPATH, '//*[@id="main"]/div[2]/div/div[1]/div[4]/div[2]/div/div/div[1]/div/label/div')
    # Элемент карточки книги "Текст" для проверки
    ELEMENT_BOOK_TEXT = (By.XPATH, '//div[text()="Текст"]')
    # Ничего не найдено
    NO_RESULTS_MESSAGE = (By.XPATH, '//*[@id="main"]/div/div[2]/div/h1')
    # Кнопка "Показать еще"
    LOAD_MORE_BUTTON = (By.XPATH, '//*[@id="main"]/div[2]')
    # Элемент карточки книги "Автор" для проверки
    ELEMENT_BOOK_AUTHOR = (By.XPATH, '//a[contains(text(), "Лукьяненко")]')
    # Элемент вижка "Высокя оцена"
    ELEMENT_AUDIO_BOOK = (By.CSS_SELECTOR, '#art_types-audiobook')

    def search_on_page(self, search_query: str):
        """Поиск на текущей странице"""
        with allure.step(f"Поиск на странице: '{search_query}'"):
            search_input = self.wait.until(
                EC.element_to_be_clickable(self.SEARCH_INPUT)
            )
            search_input.clear()
            search_input.send_keys(search_query)
            search_input.send_keys(Keys.ENTER)

            wait = WebDriverWait(self.driver, 10)
            # Ожидание исчезновения индикатора загрузки
            wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loader, .spinner, .loading"))
            )

    def search_audio(self):
        """Поиск на текущей странице фильтра аудио """
        with allure.step(f"Поиск на странице фльтра по аудокнигам "):
            search_audio = self.wait.until(
                EC.element_to_be_clickable(self.ELEMENT_AUDIO_BOOK)
            )
            # Скроллим к элементу
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_audio)

            # Небольшая пауза для стабилизации анимаций
            time.sleep(0.5)

            # Пробуем обычный клик
            try:
                search_audio.click()
            except ElementClickInterceptedException:
                # Фоллбэк: клик через JS
                allure.step("Обычный клик не сработал, используем JavaScript")
                self.driver.execute_script("arguments[0].click();", search_audio)

            wait = WebDriverWait(self.driver, 10)
            # Ожидание исчезновения индикатора загрузки
            wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loader, .spinner, .loading"))
            )

    def get_book_titles(self):
        """Получение списка названий книг на странице"""
        with allure.step("Получение списка названий книг"):
            titles_elements = self.driver.find_elements(*self.BOOK_TITLES)
            titles = [elem.text.strip() for elem in titles_elements if elem.text.strip()]
            logger.info(f"Found {len(titles)} book titles")
            return titles

    def is_no_results_displayed(self):
        """Проверка отображения сообщения об отсутствии результатов"""
        return self.is_element_displayed(self.NO_RESULTS_MESSAGE, timeout=2)

    def load_more_results(self):
        """Загрузка дополнительных результатов через кнопку 'Показать ещё' """
        with allure.step("Загрузка дополнительных результатов"):
            search_more = self.wait.until(
                EC.element_to_be_clickable(self.LOAD_MORE_BUTTON)
            )
            # Скроллим к элементу
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_more)

            # Небольшая пауза для стабилизации анимаций
            time.sleep(0.5)

            # Пробуем обычный клик
            try:
                search_more.click()
            except ElementClickInterceptedException:
                # Фоллбэк: клик через JS
                allure.step("Обычный клик не сработал, используем JavaScript")
                self.driver.execute_script("arguments[0].click();", search_more)

            wait = WebDriverWait(self.driver, 10)
            # Ожидание исчезновения индикатора загрузки
            wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loader, .spinner, .loading"))
            )

            # if self.is_element_present(self.LOAD_MORE_BUTTON, timeout=2):
            #     self.click_element(self.LOAD_MORE_BUTTON)
            #     self.wait_for_page_load()
            #     logger.info("Loaded more results")
            #     return True
            # return False

    def are_books_with_keyword_present(self, keyword: str):
        """Проверка наличия книг с ключевым словом в названии"""
        with allure.step(f"Проверка наличия книг со словом '{keyword}' в названии"):
            titles = self.is_element_displayed(self.BOOK_TITLES_ALL)
            found_books = [title for title in titles if keyword.lower() in title.lower()]
            logger.info(f"Found {len(found_books)} books with keyword '{keyword}'")
            return len(found_books) > 0

    def click_on_book_with_keyword(self, keyword: str):
        """Клик по первой книге, содержащей ключевое слово в названии"""
        with allure.step(f"Клик по книге со словом '{keyword}' в названии"):
            # Ищем элемент, содержащий текст (используем contains для гибкости)
            locator = (By.XPATH, f"//a[contains(text(), '{keyword}')]")
            try:
                element = self.wait_for_element_clickable(locator, timeout=5)
                # Прокрутка и клик через JS для надежности
                self.driver.execute_script("arguments[0].click();", element)
                self.wait_for_page_load()
                logger.info(f"Clicked on book containing: '{keyword}'")
            except TimeoutException:
                 raise AssertionError(f"No books found with keyword '{keyword}'")
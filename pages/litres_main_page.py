from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure
import time


class LitresMainPage(BasePage):
    """
    Главная страница Litres.ru
    """

    # Более надежные локаторы для поля поиска
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[data-testid='search-input']")
    SEARCH_INPUT_ALT = (By.CSS_SELECTOR, ".search-field__input")
    SEARCH_INPUT_ALT2 = (By.CSS_SELECTOR, "input[type='search']")
    SEARCH_INPUT_ALT3 = (By.CSS_SELECTOR, "input[name='q']")

    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[data-testid='search-button']")
    SEARCH_BUTTON_ALT = (By.CSS_SELECTOR, ".search-field__button")

    POPULAR_TAB = (By.XPATH, "//a[contains(@href, '/popular/')]")
    POPULAR_TAB_ALT = (By.XPATH, "//span[contains(text(), 'Популярное')]/parent::a")
    POPULAR_TAB_ALT2 = (By.XPATH, "//a[contains(text(), 'Популярное')]")

    COOKIE_ACCEPT_BUTTON = (By.XPATH, "//button[contains(text(), 'Принять')]")
    COOKIE_ACCEPT_BUTTON_ALT = (By.XPATH, "//button[contains(text(), 'Согласен')]")

    def open(self):
        """Открытие главной страницы"""
        with allure.step("Открыть главную страницу Litres.ru"):
            self.open_url("https://www.litres.ru/")
            time.sleep(2)  # Даем время на загрузку страницы
            self.accept_cookies_if_present()

    def accept_cookies_if_present(self):
        """Принять куки если они есть"""
        with allure.step("Принять cookies"):
            try:
                if self.is_element_present(self.COOKIE_ACCEPT_BUTTON, timeout=3):
                    self.click(self.COOKIE_ACCEPT_BUTTON)
                    self.logger.info("Cookies accepted")
                elif self.is_element_present(self.COOKIE_ACCEPT_BUTTON_ALT, timeout=2):
                    self.click(self.COOKIE_ACCEPT_BUTTON_ALT)
                    self.logger.info("Cookies accepted")
            except Exception as e:
                self.logger.info(f"No cookie banner present: {e}")

    def go_to_popular(self):
        """Переход на вкладку 'Популярное'"""
        with allure.step("Перейти на вкладку 'Популярное'"):
            try:
                if self.is_element_present(self.POPULAR_TAB, timeout=5):
                    self.click(self.POPULAR_TAB)
                elif self.is_element_present(self.POPULAR_TAB_ALT, timeout=3):
                    self.click(self.POPULAR_TAB_ALT)
                elif self.is_element_present(self.POPULAR_TAB_ALT2, timeout=3):
                    self.click(self.POPULAR_TAB_ALT2)
                else:
                    # Пробуем найти по тексту
                    popular_link = self.find_element((By.LINK_TEXT, "Популярное"))
                    popular_link.click()

                time.sleep(2)
                self.wait_for_page_load()
                self.logger.info("Navigated to Popular page")
            except Exception as e:
                self.logger.error(f"Failed to navigate to Popular: {e}")
                raise

    def wait_for_search_input(self, timeout=10):
        """
        Ожидание появления поля поиска с несколькими вариантами локаторов

        Args:
            timeout: время ожидания в секундах
        """
        with allure.step("Ожидание поля поиска"):
            start_time = time.time()
            while time.time() - start_time < timeout:
                for locator in [self.SEARCH_INPUT, self.SEARCH_INPUT_ALT,
                                self.SEARCH_INPUT_ALT2, self.SEARCH_INPUT_ALT3]:
                    try:
                        element = self.wait_for_clickable(locator, timeout=2)
                        if element and element.is_enabled():
                            self.logger.info(f"Search input found with locator: {locator}")
                            return element
                    except:
                        continue
                time.sleep(0.5)

            # Если не нашли, делаем скриншот для отладки
            self.take_screenshot("search_input_not_found")
            raise Exception("Search input not found on page")

    def search(self, query: str):
        """Поиск книг по запросу"""
        with allure.step(f"Поиск книг по запросу: '{query}'"):
            try:
                # Ждем появления поля поиска
                search_input = self.wait_for_search_input()

                # Очищаем поле и вводим запрос
                search_input.clear()
                search_input.send_keys(query)
                time.sleep(0.5)

                # Ищем кнопку поиска
                try:
                    if self.is_element_present(self.SEARCH_BUTTON, timeout=3):
                        self.click(self.SEARCH_BUTTON)
                    elif self.is_element_present(self.SEARCH_BUTTON_ALT, timeout=2):
                        self.click(self.SEARCH_BUTTON_ALT)
                    else:
                        # Если кнопки нет, нажимаем Enter
                        search_input.submit()
                except Exception as e:
                    self.logger.warning(f"Search button not found, using Enter: {e}")
                    search_input.submit()

                # Ждем загрузки страницы результатов
                time.sleep(2)
                self.wait_for_page_load()
                self.logger.info(f"Search executed for: {query}")

                # Делаем скриншот после поиска
                self.take_screenshot(f"search_results_{query}")

            except Exception as e:
                self.logger.error(f"Search failed: {e}")
                self.take_screenshot("search_failed")
                raise
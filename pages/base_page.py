import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from typing import List, Optional, Union, Tuple
import allure


class BasePage:
    """
    Базовый класс для всех страниц в проекте.
    Содержит общие методы для работы с элементами и взаимодействия с браузером.
    """

    def __init__(self, driver, base_url: str = None):
        """
        Инициализация базовой страницы

        Args:
            driver: экземпляр WebDriver
            base_url: базовый URL приложения
        """
        self.driver = driver
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

        # Таймауты по умолчанию (в секундах)
        self.default_timeout = 10
        self.short_timeout = 3

    # ==================== Ожидания ====================

    def wait_for_element(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        Ожидание появления элемента

        Args:
            locator: кортеж (By.ID, "value")
            timeout: время ожидания в секундах

        Returns:
            WebElement: найденный элемент
        """
        timeout = timeout or self.default_timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.info(f"Element found: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            raise

    def wait_for_clickable(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        Ожидание кликабельности элемента

        Args:
            locator: кортеж (By.ID, "value")
            timeout: время ожидания в секундах

        Returns:
            WebElement: кликабельный элемент
        """
        timeout = timeout or self.default_timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            self.logger.info(f"Element is clickable: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not clickable: {locator}")
            raise

    def wait_for_visible(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        Ожидание видимости элемента

        Args:
            locator: кортеж (By.ID, "value")
            timeout: время ожидания в секундах

        Returns:
            WebElement: видимый элемент
        """
        timeout = timeout or self.default_timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.info(f"Element is visible: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible: {locator}")
            raise

    def wait_for_invisible(self, locator: tuple, timeout: int = None) -> bool:
        """
        Ожидание исчезновения элемента

        Args:
            locator: кортеж (By.ID, "value")
            timeout: время ожидания в секундах

        Returns:
            bool: True если элемент исчез
        """
        timeout = timeout or self.default_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            self.logger.info(f"Element is invisible: {locator}")
            return True
        except TimeoutException:
            self.logger.error(f"Element still visible: {locator}")
            return False

    def wait_for_text_present(self, locator: tuple, text: str, timeout: int = None) -> bool:
        """
        Ожидание появления текста в элементе

        Args:
            locator: кортеж (By.ID, "value")
            text: ожидаемый текст
            timeout: время ожидания в секундах

        Returns:
            bool: True если текст появился
        """
        timeout = timeout or self.default_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            self.logger.info(f"Text '{text}' found in element: {locator}")
            return True
        except TimeoutException:
            self.logger.error(f"Text '{text}' not found in element: {locator}")
            return False

    # ==================== Поиск элементов ====================

    def find_element(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        Поиск элемента с ожиданием

        Args:
            locator: кортеж (By.ID, "value")
            timeout: время ожидания в секундах

        Returns:
            WebElement: найденный элемент
        """
        return self.wait_for_element(locator, timeout)

    def find_elements(self, locator: tuple, timeout: int = None) -> List[WebElement]:
        """
        Поиск всех элементов

        Args:
            locator: кортеж (By.ID, "value")
            timeout: время ожидания в секундах

        Returns:
            List[WebElement]: список найденных элементов
        """
        timeout = timeout or self.default_timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            elements = self.driver.find_elements(*locator)
            self.logger.info(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            self.logger.warning(f"No elements found: {locator}")
            return []

    def is_element_present(self, locator: tuple, timeout: int = None) -> bool:
        """
        Проверка наличия элемента на странице

        Args:
            locator: кортеж (By.ID, "value")
            timeout: время ожидания в секундах

        Returns:
            bool: True если элемент присутствует
        """
        timeout = timeout or self.short_timeout
        try:
            self.wait_for_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_element_visible(self, locator: tuple, timeout: int = None) -> bool:
        """
        Проверка видимости элемента

        Args:
            locator: кортеж (By.ID, "value")
            timeout: время ожидания в секундах

        Returns:
            bool: True если элемент видим
        """
        timeout = timeout or self.short_timeout
        try:
            self.wait_for_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    # ==================== Действия с элементами ====================

    def click(self, locator: tuple, timeout: int = None) -> None:
        """
        Клик по элементу

        Args:
            locator: кортеж (By.ID, "value")
            timeout: время ожидания в секундах
        """
        element = self.wait_for_clickable(locator, timeout)
        try:
            self.highlight_element(element)
            element.click()
            self.logger.info(f"Clicked on element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to click on element {locator}: {e}")
            # Пробуем кликнуть через JavaScript
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"Clicked via JavaScript: {locator}")

    def double_click(self, locator: tuple, timeout: int = None) -> None:
        """
        Двойной клик по элементу

        Args:
            locator: кортеж (By.ID, "value")
            timeout: время ожидания в секундах
        """
        element = self.wait_for_clickable(locator, timeout)
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.logger.info(f"Double clicked on element: {locator}")

    def right_click(self, locator: tuple, timeout: int = None) -> None:
        """
        Клик правой кнопкой мыши

        Args:
            locator: кортеж (By.ID, "value")
            timeout: время ожидания в секундах
        """
        element = self.wait_for_clickable(locator, timeout)
        actions = ActionChains(self.driver)
        actions.context_click(element).perform()
        self.logger.info(f"Right clicked on element: {locator}")

    def input_text(self, locator: tuple, text: str, clear_first: bool = True, timeout: int = None) -> None:
        """
        Ввод текста в поле

        Args:
            locator: кортеж (By.ID, "value")
            text: вводимый текст
            clear_first: очищать ли поле перед вводом
            timeout: время ожидания в секундах
        """
        element = self.wait_for_element(locator, timeout)
        self.highlight_element(element)

        if clear_first:
            element.clear()

        element.send_keys(text)
        self.logger.info(f"Entered text '{text}' into element: {locator}")

    def get_text(self, locator: tuple, timeout: int = None) -> str:
        """
        Получение текста элемента

        Args:
            locator: кортеж (By.ID, "value")
            timeout: время ожидания в секундах

        Returns:
            str: текст элемента
        """
        element = self.wait_for_visible(locator, timeout)
        text = element.text
        self.logger.info(f"Got text from {locator}: {text}")
        return text

    def get_attribute(self, locator: tuple, attribute: str, timeout: int = None) -> str:
        """
        Получение атрибута элемента

        Args:
            locator: кортеж (By.ID, "value")
            attribute: имя атрибута
            timeout: время ожидания в секундах

        Returns:
            str: значение атрибута
        """
        element = self.wait_for_element(locator, timeout)
        value = element.get_attribute(attribute)
        self.logger.info(f"Got attribute '{attribute}' from {locator}: {value}")
        return value

    def select_checkbox(self, locator: tuple, check: bool = True, timeout: int = None) -> None:
        """
        Установка/снятие чекбокса

        Args:
            locator: кортеж (By.ID, "value")
            check: True - установить, False - снять
            timeout: время ожидания в секундах
        """
        element = self.wait_for_clickable(locator, timeout)
        is_selected = element.is_selected()

        if check and not is_selected:
            element.click()
            self.logger.info(f"Checkbox checked: {locator}")
        elif not check and is_selected:
            element.click()
            self.logger.info(f"Checkbox unchecked: {locator}")

    def select_from_dropdown_by_text(self, locator: tuple, text: str, timeout: int = None) -> None:
        """
        Выбор из выпадающего списка по тексту

        Args:
            locator: кортеж (By.ID, "value")
            text: текст для выбора
            timeout: время ожидания в секундах
        """
        from selenium.webdriver.support.ui import Select

        element = self.wait_for_element(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(text)
        self.logger.info(f"Selected '{text}' from dropdown: {locator}")

    def select_from_dropdown_by_value(self, locator: tuple, value: str, timeout: int = None) -> None:
        """
        Выбор из выпадающего списка по значению

        Args:
            locator: кортеж (By.ID, "value")
            value: значение для выбора
            timeout: время ожидания в секундах
        """
        from selenium.webdriver.support.ui import Select

        element = self.wait_for_element(locator, timeout)
        select = Select(element)
        select.select_by_value(value)
        self.logger.info(f"Selected value '{value}' from dropdown: {locator}")

    # ==================== Работа с JavaScript ====================

    def execute_script(self, script: str, *args) -> object:
        """
        Выполнение JavaScript

        Args:
            script: JavaScript код
            *args: аргументы для скрипта

        Returns:
            object: результат выполнения скрипта
        """
        return self.driver.execute_script(script, *args)

    def scroll_to_element(self, locator: tuple, timeout: int = None) -> None:
        """
        Прокрутка к элементу

        Args:
            locator: кортеж (By.ID, "value")
            timeout: время ожидания в секундах
        """
        element = self.wait_for_element(locator, timeout)
        self.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.info(f"Scrolled to element: {locator}")

    def scroll_to_top(self) -> None:
        """Прокрутка вверх страницы"""
        self.execute_script("window.scrollTo(0, 0);")
        self.logger.info("Scrolled to top")

    def scroll_to_bottom(self) -> None:
        """Прокрутка вниз страницы"""
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.logger.info("Scrolled to bottom")

    def highlight_element(self, element: WebElement, duration: int = 2) -> None:
        """
        Подсветка элемента (для отладки)

        Args:
            element: элемент для подсветки
            duration: длительность подсветки в секундах
        """
        self.execute_script(
            "arguments[0].style.border='3px solid red';",
            element
        )

        def remove_highlight():
            self.execute_script(
                "arguments[0].style.border='';",
                element
            )

        # Убираем подсветку через duration секунд
        self.driver.execute_script(
            f"setTimeout(function() {{ arguments[0].style.border=''; }}, {duration * 1000});",
            element
        )

    # ==================== Работа с окнами и вкладками ====================

    def switch_to_window(self, window_index: int = 0) -> None:
        """
        Переключение на окно по индексу

        Args:
            window_index: индекс окна
        """
        windows = self.driver.window_handles
        if window_index < len(windows):
            self.driver.switch_to.window(windows[window_index])
            self.logger.info(f"Switched to window index: {window_index}")
        else:
            self.logger.error(f"Window index {window_index} not found")

    def switch_to_new_window(self) -> None:
        """Переключение на последнее открытое окно"""
        current_window = self.driver.current_window_handle
        windows = self.driver.window_handles

        for window in windows:
            if window != current_window:
                self.driver.switch_to.window(window)
                self.logger.info("Switched to new window")
                return

    def close_current_window(self) -> None:
        """Закрытие текущего окна"""
        self.driver.close()
        self.logger.info("Closed current window")

    # ==================== Работа с iframe ====================

    def switch_to_iframe(self, locator: tuple, timeout: int = None) -> None:
        """
        Переключение на iframe

        Args:
            locator: кортеж (By.ID, "value")
            timeout: время ожидания в секундах
        """
        iframe = self.wait_for_element(locator, timeout)
        self.driver.switch_to.frame(iframe)
        self.logger.info(f"Switched to iframe: {locator}")

    def switch_to_default_content(self) -> None:
        """Переключение на основной контент страницы"""
        self.driver.switch_to.default_content()
        self.logger.info("Switched to default content")

    # ==================== Навигация ====================

    def open_url(self, url: str = None) -> None:
        """
        Открытие URL

        Args:
            url: URL для открытия (если не указан, используется base_url)
        """
        if url is None:
            url = self.base_url

        if not url:
            raise ValueError("URL is not provided")

        self.driver.get(url)
        self.logger.info(f"Opened URL: {url}")
        self.wait_for_page_load()

    def wait_for_page_load(self, timeout: int = 15) -> None:
        """
        Ожидание загрузки страницы

        Args:
            timeout: время ожидания в секундах
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            self.logger.info("Page loaded")
        except TimeoutException:
            self.logger.warning("Page load timeout")

    def refresh_page(self) -> None:
        """Обновление страницы"""
        self.driver.refresh()
        self.logger.info("Page refreshed")
        self.wait_for_page_load()

    def go_back(self) -> None:
        """Назад в истории"""
        self.driver.back()
        self.logger.info("Navigated back")

    def go_forward(self) -> None:
        """Вперед в истории"""
        self.driver.forward()
        self.logger.info("Navigated forward")

    # ==================== Скриншоты ====================

    def take_screenshot(self, name: str = "screenshot") -> bytes:
        """
        Создание скриншота

        Args:
            name: имя скриншота

        Returns:
            bytes: скриншот в формате PNG
        """
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        self.logger.info(f"Screenshot taken: {name}")
        return screenshot

    # ==================== Работа с куками ====================

    def get_cookie(self, name: str) -> dict:
        """
        Получение куки по имени

        Args:
            name: имя куки

        Returns:
            dict: кука
        """
        return self.driver.get_cookie(name)

    def set_cookie(self, cookie: dict) -> None:
        """
        Установка куки

        Args:
            cookie: словарь с параметрами куки
        """
        self.driver.add_cookie(cookie)
        self.logger.info(f"Cookie set: {cookie}")

    def delete_cookie(self, name: str) -> None:
        """
        Удаление куки

        Args:
            name: имя куки
        """
        self.driver.delete_cookie(name)
        self.logger.info(f"Cookie deleted: {name}")

    def delete_all_cookies(self) -> None:
        """Удаление всех кук"""
        self.driver.delete_all_cookies()
        self.logger.info("All cookies deleted")

    # ==================== Вспомогательные методы ====================

    def wait_for_ajax(self, timeout: int = 10) -> None:
        """
        Ожидание завершения AJAX запросов

        Args:
            timeout: время ожидания в секундах
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return jQuery.active == 0")
            )
            self.logger.info("AJAX requests completed")
        except:
            self.logger.debug("No jQuery found or AJAX timeout")

    def is_page_opened(self, expected_title: str = None, expected_url: str = None) -> bool:
        """
        Проверка, что страница открыта

        Args:
            expected_title: ожидаемый заголовок
            expected_url: ожидаемый URL

        Returns:
            bool: True если страница соответствует ожиданиям
        """
        if expected_title:
            return self.driver.title == expected_title

        if expected_url:
            return expected_url in self.driver.current_url

        return True
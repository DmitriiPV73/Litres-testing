from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, timeout)

    def open_url(self, url):
        """Открываем страницы по url"""
        self.driver.get(url)
        return self

    def wait_for_page_load(self, timeout=None):
        """Ожидание полной загрузки страницы"""
        if timeout is None:
            timeout = self.timeout
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return self

    def find_element(self, locator, timeout=5):
        """Поиск элемента с ожиданием"""
        if timeout is None:
            timeout = self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def is_element_present(self, locator, timeout=None) -> bool:
        """Проверка наличия элемента в DOM (не обязательно видимого)"""
        if timeout is None:
            timeout = self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_clickable(self, locator, timeout=5):
        """Ожидание кликабельности элемента"""
        if timeout is None:
            timeout = self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_element_visible(self, locator, timeout=None):
        """Ожидание видимости элемента"""
        if timeout is None:
            timeout = self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def is_element_displayed(self, locator, timeout=None):
        """Проверка, отображается ли элемент"""
        if timeout is None:
            timeout = self.timeout
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    def click_element(self, locator, timeout=None):
        """Клик по элементу с ожиданием"""
        element = self.wait_for_element_clickable(locator, timeout)
        element.click()

    def input_text(self, locator, text, timeout=None):
        """Ввод текста в поле с ожиданием"""
        element = self.wait_for_element_clickable(locator, timeout)
        element.clear()
        element.send_keys(text)
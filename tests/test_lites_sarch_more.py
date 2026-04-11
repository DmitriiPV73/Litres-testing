"""Тест предназначен для получения дополнительнго списка книг по кнопке 'Показать еще' в разделе Популярное на Litres"""
import pytest
import allure
import logging
from selenium.webdriver.common.by import By
from selenium import webdriver
from pages.main_page import MainPage
from pages.search_page import SearchResultsPage

logger = logging.getLogger(__name__)

@allure.feature("Поиск книг на Litres.ru")
@pytest.mark.parametrize("browser", ["Chrome", "Firefox"], indirect=True)
class TestSearch:
    """Тесты функционала поиска на сайте Litres.ru"""

    @allure.story("Поиск автора в разделе 'Популярное'")
    @allure.title("Проверка загрузки книг по кнопке 'Показать еще'")
    @allure.description("""
        1. Открыть главную страницу Litres.ru
        2. Перейти в раздел 'Популярное'
        3. Нажимаем 'Показать еще'
        4. Ждем загрузки книг
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_more_in_popular(self, browser):
        """
        Интеграционный тест: переход в Популярное → поиск автора → проверка результатов
        """
        main_page = MainPage(browser)
        search_page = SearchResultsPage(browser)

        with allure.step("Открыть главную страницу и перейти в раздел 'Популярное'"):
            main_page.open()
            main_page.go_to_tab()
            main_page.is_popular_page_loaded()

        with allure.step("Выполнить переход по 'Показать еще'"):
            search_page.load_more_results()
            screenshot = browser.get_screenshot_as_png()
            allure.attach(screenshot, name="page_more")




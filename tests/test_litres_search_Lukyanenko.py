"""Тест предназначен для получения списка книг автора Лукьяненко в разделе Популярное на Litres"""
import time

import pytest
import allure
import logging
from pages.main_page import MainPage
from pages.search_page import SearchResultsPage

logger = logging.getLogger(__name__)

@allure.feature("Поиск книг на Litres.ru")
class TestSearch:
    """Тесты функционала поиска на сайте Litres.ru"""

    @allure.story("Поиск автора в разделе 'Популярное'")
    @allure.title("Проверка поиска книг автора 'Лукьяненко'")
    @allure.description("""
        1. Открыть главную страницу Litres.ru
        2. Перейти в раздел 'Популярное'
        3. Ввести в поиск 'Лукьяненко'
        4. Проверить, что результаты содержат книги автора
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_lukyanenko_in_popular(self, browser):
        """
        Интеграционный тест: переход в Популярное → поиск автора → проверка результатов
        """
        main_page = MainPage(browser)
        search_page = SearchResultsPage(browser)
        search_query = "Лукьяненко"

        with allure.step("Открыть главную страницу и перейти в раздел 'Популярное'"):
            main_page.open()
            main_page.go_to_tab()
            main_page.is_popular_page_loaded()

        with allure.step(f"Выполнить поиск по запросу: '{search_query}'"):
            search_page.search_on_page(search_query)
            screenshot = browser.get_screenshot_as_png()
            allure.attach(screenshot, name="page_Lukyanenko")

        with allure.step("Проверка отображения сообщения об отсутствии результатов"):
            assert  not search_page.is_no_results_displayed(), "Ничего не найдено"

        with allure.step("Получение списка названий книг на странице"):
            search_page.get_book_titles()
            titles = search_page.get_book_titles()
            print(titles)







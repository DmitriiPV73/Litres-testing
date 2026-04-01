"""
Негативный тест предназначен для получения оповещения 'Ничего не найдено'
в разделе Популярное на Litres при вводе несуществующего запроса
"""
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
    @allure.title("Проверка негативного поиска 'asdfghjkl123456'")
    @allure.description("""
        1. Открыть главную страницу Litres.ru
        2. Перейти в раздел 'Популярное'
        3. Ввести в поиск 'asdfghjkl123456'
        4. Проверить, что результат содержат уведомление 'Ничего не найдено'
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_negative_asdfghjkl123456(self, browser):
        """
        Интеграционный тест: переход в Популярное → ввод неущствующего запроса → проверка результатов
        """
        main_page = MainPage(browser)
        search_page = SearchResultsPage(browser)
        search_query = "asdfghjkl123456"

        with allure.step("Открыть главную страницу и перейти в раздел 'Популярное'"):
            main_page.open()
            main_page.go_to_tab()
            main_page.is_popular_page_loaded()

        with allure.step(f"Выполнить поиск по запросу: '{search_query}'"):
            search_page.search_on_page(search_query)
            screenshot = browser.get_screenshot_as_png()
            allure.attach(screenshot, name="page_asdfghjkl123456")

        with allure.step("Проверка отображения сообщения об отсутствии результатов"):
            assert search_page.is_no_results_displayed(), "'Ничего не найдено' не найдено"
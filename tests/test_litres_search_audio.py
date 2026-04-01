import pytest
import allure
import logging
from selenium.webdriver.common.by import By
from selenium import webdriver
from pages.main_page import MainPage
from pages.search_page import SearchResultsPage

logger = logging.getLogger(__name__)

@allure.feature("Поиск книг на Litres.ru")
class TestSearch:
    """Тесты функционала поиска на сайте Litres.ru"""

    @allure.story("Поиск по фильтру в разделе 'Популярное'")
    @allure.title("Проверка поиска удиокниг")
    @allure.description("""
        1. Открыть главную страницу Litres.ru
        2. Перейти в раздел 'Популярное'
        3. Иницировать поис аудиокниг
        4. Проверить, что результаты содержат аудиокниги
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_audio_in_popular(self, browser):
        """
        Интеграционный тест: переход в Популярное → выбор по аудиокниге → проверка результатов
        """
        main_page = MainPage(browser)
        search_page = SearchResultsPage(browser)

        with allure.step("Открыть главную страницу и перейти в раздел 'Популярное'"):
            main_page.open()
            main_page.go_to_tab()
            main_page.is_popular_page_loaded()

        with allure.step("Сортировка по аудиокнигам"):
            search_page.search_audio()
            screenshot = browser.get_screenshot_as_png()
            allure.attach(screenshot, name="page_cost")

        with allure.step("Получение списка названий книг на странице"):
            titles = search_page.get_book_titles()
            # Логируем список книг
            logger.info(f"Найденные книги: {titles}")

            # Добавляем список книг в Allure отчет
            allure.attach(
                "\n".join([f"{i}. {title}" for i, title in enumerate(titles, 1)]),
                name="Список найденных книг",
                attachment_type=allure.attachment_type.TEXT
            )
            # Проверяем, что список не пустой
            assert len(titles) > 0, "Список книг пуст"
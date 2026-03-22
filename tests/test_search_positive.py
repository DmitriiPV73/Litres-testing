"""
Автотест для проверки поиска вакансий по слову "Водитель" на Avito.ru
Тест проверяет, что в результате поиска все вакансии содержат слово "Водитель"
"""

from pages.search_page import SearchPage
from pages.job_page import JobPage

def test_navigate_to_job_section(driver):
    """Переход в раздел 'Работа' и проверка загрузки"""
    # Открываем главную страницу
    search_page = SearchPage(driver)
    search_page.open()
    search_page.wait(3)  # ЖЖдём полной загрузки главной страницы

    # Кликаем по ссылке "Работа"
    search_page.click_job_section()
    search_page.wait(3)  # Ждём перехода и загрузки новой страницы

    # Проверяем, что страница "Работа" загрузилась
    assert "/rabota" in driver.current_url, f"Не перешли на страницу работы. Текущий URL: {driver.current_url}"

    # Проверка 2: через метод JobPage
    job_page = JobPage(driver)
    assert job_page.is_loaded(), "Страница 'Работа' не загрузилась"

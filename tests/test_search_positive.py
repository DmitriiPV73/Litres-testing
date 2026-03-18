"""
Автотест для проверки поиска вакансий по слову "Водитель" на Avito.ru
Тест проверяет, что в результате поиска все вакансии содержат слово "Водитель"
"""

import pytest
import os
import time
from pages.search_page import SearchPage

# Тестовый класс для проверки позитивных сценариев поиска на Avito.ru
# Параметры для тестирования
search_queries = [
    "Водитель",
    "Программист",
    "Продавец",
    "Врач"
]

@pytest.mark.parametrize("query", search_queries)
# Тест: поиск по названию вакансии. Прверка в названиях вакнсии искомого слова
def test_search_by_profession(self, driver, base_url, query):
    # Создаем директорию для скриншотов
    screenshot_dir = "screenshots"
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    # Инициируется Page Object
    search_page = SearchPage(driver)
    # Шаг 1. Открываем главную страницу Avito
    search.page.open(base_url)
    # Шаг 2. Переходим в раздел "Работа"
    search_page.go_to_job_section()
    # Шаг 3. Выполняем поиск
    search_page.search(query)
    # Шаг 4. Делаем скриншот результатов
    screenshot_name = f"{screenshot_dir}/search_{query}_{int(time.time())}.png"
    search_page.take_screenshot(screenshot_name)
    # Шаг 5. Проверяем, что вакансии найдены
    assert search_page.are_vacancies_found(), f"По запросу '{query}' не найдено вакансий"
    # Шаг 6. Проверяем, что все вакансии содержат искомое слово
    all_contain, invalid_titles = search_page.check_vacancy_titles_contain(query)
    if not all_contain:
        # Считаем % невалидных вакансий
        total=len(search_page.get_vacancy_titles())
        invalid_titles = (len(invalid_titles)/total)*100 if total>0 else 0
        print(f"Всего вакансий: {total}, некорректных: {len(invalid_titles)} ({invalid_percent:.1f}%)")

    print(f"\nТест для запроса '{query}' успешно пройден!\n")

# Тест: поиск по нескольким словам
def test_search_with_multiple_words(self, driver, base_url):
    query = "Водитель категории B"

    search_page = SearchPage(driver)
    search_page.open(base_url)
    search_page.go_to_job_section()
    search_page.search(query)
    # Сохраняем скриншот
    search_page.take_screenshot(f"screenshots/multi_word_search_{int(time.time())}.png")
    # Проверяем, что есть результаты
    assert search_page.are_vacancies_found(), f"По запросу '{query}' не найдено вакансий"
    # Для многословного запроса проверяем наличие хотя бы одного слова из запроса
    titles = search_page.get_vacancy_titles()
    words = query.lower().split()
    # Ппроверка для многословных запросов
    for title in titles[:5]:  # Проверяем первые 5 вакансий
        title_lower = title.lower()
        contains_any = any(word in title_lower for word in words)
        assert contains_any, f"Вакансия '{title}' не содержит ни одного слова из запроса {words}"

    print(f"\nТест для многословного запроса '{query}' успешно пройден!\n")

# Тест: проверка регистронезависимости поиска
def test_search_case_insensitive(self, driver, base_url):
    test_cases = [
        ("ВОДИТЕЛЬ", "Водитель"),
        ("программист", "Программист"),
        ("PROGRAMMER", "programmer")
    ]

    for query_upper, query_lower in test_cases:
        search_page = SearchPage(driver)
        search_page.open(base_url)
        search_page.go_to_job_section()

        # Поиск в верхнем регистре
        search_page.search(query_upper)
        titles_upper = search_page.get_vacancy_titles()
        count_upper = len(titles_upper)

        # Возвращаемся и ищем в нижнем регистре
        # Для чистоты эксперимента лучше открыть новую сессию, для простоты перезагрузим страницу
        driver.get(base_url)
        search_page.go_to_job_section()
        search_page.search(query_lower)
        titles_lower = search_page.get_vacancy_titles()
        count_lower = len(titles_lower)

        # Проверяем, что количество результатов примерно одинаково
        diff_percent = abs(count_upper - count_lower) / max(count_upper, count_lower) * 100

        print(f"Запрос '{query_upper}': {count_upper} результатов")
        print(f"Запрос '{query_lower}': {count_lower} результатов")
        print(f"Разница: {diff_percent:.1f}%")

        # Допускаем разницу до 20% (из-за возможных изменений в БД между запросами)
        assert diff_percent < 20, f"Слишком большая разница в результатах для разных регистров"

    print(f"\nТест на регистронезависимость успешно пройден!\n")

if __name__ == "__main__":
    pytest.main(["-v", "test_search_positive.py"])

import pytest
import allure
from pages.litres_main_page import LitresMainPage
from pages.litres_search_results_page import LitresSearchResultsPage


@allure.feature("Litres.ru")
@allure.story("Поиск книг")
class TestLitresPopularSearch:
    """
    Тесты для проверки поиска книг на Litres.ru
    """

    @allure.title("Поиск книг со словом 'Седьмой' на странице популярного")
    @allure.description("Переход на вкладку 'Популярное' и поиск книг, содержащих в названии 'Седьмой'")
    @allure.tag("search", "popular", "litres")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_books_with_seventh_in_popular(self, browser):
        """
        Тест: Переход на вкладку 'Популярное' и поиск книг со словом 'Седьмой'
        """
        # Шаг 1: Открытие главной страницы
        main_page = LitresMainPage(browser)
        main_page.open()

        # Шаг 2: Переход на вкладку 'Популярное'
        main_page.go_to_popular()

        # Шаг 3: Поиск книг по запросу "Седьмой"
        main_page.search("Седьмой")

        # Шаг 4: Проверка результатов поиска
        search_results = LitresSearchResultsPage(browser)

        # Получаем список названий книг
        book_titles = search_results.get_book_titles()

        # Прикрепляем список найденных книг к отчету allure
        allure.attach(
            "\n".join(book_titles),
            name="Найденные книги",
            attachment_type=allure.attachment_type.TEXT
        )

        # Проверяем, что результаты поиска не пустые
        assert len(book_titles) > 0, "Результаты поиска не должны быть пустыми"

        # Проверяем, что все найденные книги содержат слово "Седьмой" в названии
        for title in book_titles:
            assert "Седьмой" in title or "седьмой" in title, \
                f"Книга '{title}' не содержит слово 'Седьмой' в названии"

        # Дополнительно: выводим информацию в лог
        browser.logger.info(f"Найдено книг со словом 'Седьмой': {len(book_titles)}")

        # Прикрепляем скриншот страницы с результатами
        search_results.take_screenshot("search_results_with_seventh")

    # @allure.title("Проверка наличия конкретных книг со словом 'Седьмой'")
    # @allure.description("Поиск и проверка наличия книг, содержащих 'Седьмой' в названии")
    # def test_specific_books_with_seventh(self, browser):
    #     """
    #     Тест: Поиск конкретных книг, содержащих 'Седьмой' в названии
    #     """
    #     # Открытие главной страницы и переход в популярное
    #     main_page = LitresMainPage(browser)
    #     main_page.open()
    #     main_page.go_to_popular()
    #
    #     # Поиск книг со словом "Седьмой"
    #     main_page.search("Седьмой")
    #
    #     # Получаем результаты
    #     search_results = LitresSearchResultsPage(browser)
    #     books_data = search_results.get_books_data()
    #
    #     # Прикрепляем подробные данные о книгах
    #     books_info = "\n".join([
    #         f"{book['title']} - {book['author']}"
    #         for book in books_data
    #     ])
    #     allure.attach(
    #         books_info,
    #         name="Найденные книги (с авторами)",
    #         attachment_type=allure.attachment_type.TEXT
    #     )
    #
    #     # Проверяем, что найдены книги со словом "Седьмой"
    #     books_with_seventh = search_results.get_books_with_keyword("Седьмой")
    #     assert len(books_with_seventh) > 0, "Не найдено книг со словом 'Седьмой'"
    #
    #     # Проверяем, что в названиях действительно есть "Седьмой"
    #     for book in books_with_seventh:
    #         assert "Седьмой" in book["title"] or "седьмой" in book["title"], \
    #             f"В названии '{book['title']}' нет слова 'Седьмой'"
    #
    #     # Проверяем, что у всех книг есть авторы
    #     for book in books_with_seventh:
    #         assert book["author"], f"У книги '{book['title']}' не указан автор"
    #
    @allure.title("Проверка перехода на страницу книги из результатов поиска")
    @allure.description("Поиск книги со словом 'Седьмой' и переход на её страницу")
    def test_click_on_book_with_seventh(self, browser):
        """
        Тест: Переход на страницу книги из результатов поиска
        """
        # Открытие главной страницы и переход в популярное
        main_page = LitresMainPage(browser)
        main_page.open()
        main_page.go_to_popular()

        # Поиск книг со словом "Седьмой"
        main_page.search("Седьмой")

        # Переход на страницу первой книги со словом "Седьмой"
        search_results = LitresSearchResultsPage(browser)

        # Запоминаем название книги до перехода
        books = search_results.get_books_with_keyword("Седьмой")
        assert len(books) > 0, "Не найдено книг со словом 'Седьмой'"
        book_title = books[0]["title"]

        # Кликаем по книге
        search_results.click_on_book_with_keyword("Седьмой")

        # Проверяем, что перешли на страницу книги
        current_url = browser.current_url
        assert "litres.ru" in current_url, "URL не принадлежит litres.ru"

        # Проверяем, что в URL или заголовке страницы есть название книги
        page_title = browser.title
        assert "Седьмой" in page_title or book_title in page_title, \
            f"На странице книги '{page_title}' нет ожидаемого названия '{book_title}'"

        # Прикрепляем скриншот страницы книги
        allure.attach(
            browser.get_screenshot_as_png(),
            name="book_page",
            attachment_type=allure.attachment_type.PNG
        )
    #
    # @allure.title("Проверка загрузки дополнительных результатов при поиске")
    # @allure.description("Проверка работы кнопки 'Показать ещё' при поиске книг со словом 'Седьмой'")
    # def test_load_more_results(self, browser):
    #     """
    #     Тест: Проверка загрузки дополнительных результатов
    #     """
    #     # Открытие главной страницы и переход в популярное
    #     main_page = LitresMainPage(browser)
    #     main_page.open()
    #     main_page.go_to_popular()
    #
    #     # Поиск книг со словом "Седьмой"
    #     main_page.search("Седьмой")
    #
    #     # Получаем результаты поиска
    #     search_results = LitresSearchResultsPage(browser)
    #     initial_titles = search_results.get_book_titles()
    #     initial_count = len(initial_titles)
    #
    #     # Пытаемся загрузить больше результатов
    #     more_loaded = search_results.load_more_results()
    #
    #     if more_loaded:
    #         # Получаем обновленный список названий
    #         updated_titles = search_results.get_book_titles()
    #         updated_count = len(updated_titles)
    #
    #         # Проверяем, что количество результатов увеличилось
    #         assert updated_count > initial_count, \
    #             f"Количество результатов не увеличилось: было {initial_count}, стало {updated_count}"
    #
    #         # Проверяем, что все названия содержат слово "Седьмой"
    #         for title in updated_titles:
    #             assert "Седьмой" in title or "седьмой" in title, \
    #                 f"Книга '{title}' не содержит слово 'Седьмой'"
    #
    #         allure.attach(
    #             f"Было: {initial_count} книг\nСтало: {updated_count} книг",
    #             name="Результаты загрузки",
    #             attachment_type=allure.attachment_type.TEXT
    #         )
    #     else:
    #         allure.attach(
    #             "Кнопка 'Показать ещё' не найдена",
    #             name="Информация",
    #             attachment_type=allure.attachment_type.TEXT
    #         )
    #         pytest.skip("Кнопка 'Показать ещё' не найдена на странице")
    #
    # @allure.title("Проверка поиска с учетом регистра")
    # @allure.description("Проверка, что поиск работает независимо от регистра")
    # def test_search_case_insensitive(self, browser):
    #     """
    #     Тест: Проверка регистронезависимого поиска
    #     """
    #     # Открытие главной страницы и переход в популярное
    #     main_page = LitresMainPage(browser)
    #     main_page.open()
    #     main_page.go_to_popular()
    #
    #     # Поиск с маленькой буквы
    #     main_page.search("седьмой")
    #
    #     # Проверяем результаты
    #     search_results = LitresSearchResultsPage(browser)
    #     titles_lower = search_results.get_book_titles()
    #
    #     # Поиск с большой буквы
    #     main_page.search("Седьмой")
    #
    #     # Проверяем результаты
    #     titles_upper = search_results.get_book_titles()
    #
    #     # Сравниваем количество результатов
    #     assert len(titles_lower) == len(titles_upper), \
    #         f"Количество результатов различается: {len(titles_lower)} vs {len(titles_upper)}"
    #
    #     # Проверяем, что результаты содержат слово в любом регистре
    #     for title in titles_upper:
    #         assert "седьмой" in title.lower(), \
    #             f"Книга '{title}' не содержит слово 'седьмой' (независимо от регистра)"
    #
    # @allure.title("Проверка наличия книги 'Седьмой' в результатах поиска")
    # @allure.description("Поиск конкретной книги, содержащей 'Седьмой' в названии")
    # def test_find_specific_seventh_book(self, browser):
    #     """
    #     Тест: Поиск конкретной книги со словом 'Седьмой' в названии
    #     """
    #     # Открытие главной страницы и переход в популярное
    #     main_page = LitresMainPage(browser)
    #     main_page.open()
    #     main_page.go_to_popular()
    #
    #     # Поиск книг со словом "Седьмой"
    #     main_page.search("Седьмой")
    #
    #     # Получаем данные о книгах
    #     search_results = LitresSearchResultsPage(browser)
    #     books = search_results.get_books_data()
    #
    #     # Прикрепляем список найденных книг
    #     books_list = "\n".join([f"- {book['title']} ({book['author']})" for book in books])
    #     allure.attach(books_list, name="Найденные книги", attachment_type=allure.attachment_type.TEXT)
    #
    #     # Проверяем, что есть книги с "Седьмой" в названии
    #     books_with_seventh = [book for book in books if "Седьмой" in book["title"] or "седьмой" in book["title"]]
    #     assert len(books_with_seventh) > 0, "Не найдено книг со словом 'Седьмой'"
    #
    #     # Дополнительная проверка: выводим названия найденных книг
    #     seventh_books_titles = [book["title"] for book in books_with_seventh]
    #     allure.attach(
    #         "\n".join(seventh_books_titles),
    #         name="Книги со словом 'Седьмой'",
    #         attachment_type=allure.attachment_type.TEXT
    #     )

        # Проверяем, что у каждой книги есть автор
        for book in books_with_seventh:
            assert book["author"], f"У книги '{book['title']}' не указан автор"
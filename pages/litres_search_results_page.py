from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from typing import List, Dict
import allure


class LitresSearchResultsPage(BasePage):
    """
    Страница результатов поиска Litres.ru
    """

    # Локаторы элементов
    BOOK_CARDS = (By.CSS_SELECTOR, "article[data-testid='art'], .art-item, .book-item")
    BOOK_TITLES = (By.CSS_SELECTOR, "a[data-testid='art-title'], .art-title, .book-title")
    BOOK_AUTHORS = (By.CSS_SELECTOR, "a[data-testid='art-author'], .art-author")
    BOOK_LINKS = (By.CSS_SELECTOR, "a[data-testid='art-title']")
    LOAD_MORE_BUTTON = (By.XPATH, "//button[contains(text(), 'Показать ещё')]")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[data-testid='search-input'], .search-field__input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[data-testid='search-button']")
    NO_RESULTS_MESSAGE = (By.XPATH, "//div[contains(text(), 'Ничего не найдено')]")

    def get_book_titles(self) -> List[str]:
        """
        Получение списка названий книг на странице

        Returns:
            List[str]: список названий книг
        """
        with allure.step("Получение списка названий книг"):
            titles_elements = self.find_elements(self.BOOK_TITLES)
            titles = [elem.text.strip() for elem in titles_elements if elem.text.strip()]
            self.logger.info(f"Found {len(titles)} book titles")
            return titles

    def get_books_data(self) -> List[Dict[str, str]]:
        """
        Получение данных о книгах (название, автор, ссылка)

        Returns:
            List[Dict[str, str]]: список словарей с данными книг
        """
        with allure.step("Получение данных о книгах"):
            books = []
            book_cards = self.find_elements(self.BOOK_CARDS)

            for card in book_cards:
                try:
                    # Находим название в карточке
                    title_element = card.find_element(By.CSS_SELECTOR, "a[data-testid='art-title'], .art-title")
                    title = title_element.text.strip()

                    # Находим автора
                    author_element = card.find_element(By.CSS_SELECTOR, "a[data-testid='art-author'], .art-author")
                    author = author_element.text.strip()

                    # Находим ссылку
                    link = title_element.get_attribute("href")

                    books.append({
                        "title": title,
                        "author": author,
                        "link": link
                    })
                except:
                    continue

            self.logger.info(f"Retrieved data for {len(books)} books")
            return books

    def search_on_page(self, query: str):
        """
        Поиск на текущей странице (если есть поле поиска)

        Args:
            query: поисковый запрос
        """
        with allure.step(f"Поиск на странице: '{query}'"):
            search_input = self.wait_for_clickable(self.SEARCH_INPUT)
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys(Keys.RETURN)
            self.wait_for_page_load()
            self.logger.info(f"Search executed on page: {query}")

    def load_more_results(self):
        """Загрузка дополнительных результатов (если есть кнопка 'Показать ещё')"""
        with allure.step("Загрузка дополнительных результатов"):
            if self.is_element_present(self.LOAD_MORE_BUTTON, timeout=2):
                self.click(self.LOAD_MORE_BUTTON)
                self.wait_for_page_load()
                self.logger.info("Loaded more results")
                return True
            return False

    def are_books_with_keyword_present(self, keyword: str) -> bool:
        """
        Проверка наличия книг с ключевым словом в названии

        Args:
            keyword: ключевое слово для поиска в названиях

        Returns:
            bool: True если найдены книги с ключевым словом
        """
        with allure.step(f"Проверка наличия книг со словом '{keyword}' в названии"):
            titles = self.get_book_titles()
            found_books = [title for title in titles if keyword.lower() in title.lower()]
            self.logger.info(f"Found {len(found_books)} books with keyword '{keyword}'")
            return len(found_books) > 0

    def get_books_with_keyword(self, keyword: str) -> List[Dict[str, str]]:
        """
        Получение книг, содержащих ключевое слово в названии

        Args:
            keyword: ключевое слово для поиска в названиях

        Returns:
            List[Dict[str, str]]: список книг, содержащих ключевое слово
        """
        with allure.step(f"Поиск книг со словом '{keyword}' в названии"):
            all_books = self.get_books_data()
            filtered_books = [book for book in all_books if keyword.lower() in book["title"].lower()]
            self.logger.info(f"Found {len(filtered_books)} books with keyword '{keyword}'")
            return filtered_books

    def click_on_book_with_keyword(self, keyword: str) -> None:
        """
        Клик по первой книге, содержащей ключевое слово в названии

        Args:
            keyword: ключевое слово для поиска в названиях
        """
        with allure.step(f"Клик по книге со словом '{keyword}' в названии"):
            books = self.get_books_with_keyword(keyword)
            if books:
                self.driver.get(books[0]["link"])
                self.wait_for_page_load()
                self.logger.info(f"Clicked on book: {books[0]['title']}")
            else:
                raise AssertionError(f"No books found with keyword '{keyword}'")

    def is_no_results_displayed(self) -> bool:
        """
        Проверка отображения сообщения об отсутствии результатов

        Returns:
            bool: True если сообщение отображается
        """
        return self.is_element_present(self.NO_RESULTS_MESSAGE, timeout=2)
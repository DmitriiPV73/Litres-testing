from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from typing import List, Dict, Optional
import allure


class SearchPage(BasePage):
    """
    Страница поиска
    """

    # ==================== Локаторы элементов ====================

    # Поле поиска
    SEARCH_INPUT = (By.ID, "search-input")
    SEARCH_BUTTON = (By.XPATH, "//button[@type='submit']")
    SEARCH_ICON = (By.CSS_SELECTOR, ".search-icon")

    # Результаты поиска
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".search-results .result-item")
    SEARCH_RESULT_TITLES = (By.CSS_SELECTOR, ".result-item .title")
    SEARCH_RESULT_DESCRIPTIONS = (By.CSS_SELECTOR, ".result-item .description")
    SEARCH_RESULT_LINKS = (By.CSS_SELECTOR, ".result-item a")

    # Фильтры поиска
    FILTER_CATEGORY = (By.CSS_SELECTOR, ".filter-category")
    FILTER_PRICE = (By.CSS_SELECTOR, ".filter-price")
    FILTER_RATING = (By.CSS_SELECTOR, ".filter-rating")
    APPLY_FILTERS_BUTTON = (By.CSS_SELECTOR, ".apply-filters")
    CLEAR_FILTERS_BUTTON = (By.CSS_SELECTOR, ".clear-filters")

    # Пагинация
    PAGINATION_NEXT = (By.CSS_SELECTOR, ".pagination .next")
    PAGINATION_PREV = (By.CSS_SELECTOR, ".pagination .prev")
    PAGINATION_PAGES = (By.CSS_SELECTOR, ".pagination .page-number")
    CURRENT_PAGE = (By.CSS_SELECTOR, ".pagination .current-page")

    # Сообщения
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, ".no-results-message")
    SEARCH_SUMMARY = (By.CSS_SELECTOR, ".search-summary")
    LOADING_INDICATOR = (By.CSS_SELECTOR, ".loading-spinner")

    # Сортировка
    SORT_DROPDOWN = (By.CSS_SELECTOR, ".sort-select")
    SORT_BY_RELEVANCE = (By.XPATH, "//option[text()='Relevance']")
    SORT_BY_PRICE_ASC = (By.XPATH, "//option[text()='Price: Low to High']")
    SORT_BY_PRICE_DESC = (By.XPATH, "//option[text()='Price: High to Low']")
    SORT_BY_RATING = (By.XPATH, "//option[text()='Rating']")

    # Автодополнение
    AUTOCOMPLETE_SUGGESTIONS = (By.CSS_SELECTOR, ".autocomplete-suggestions")
    AUTOCOMPLETE_ITEM = (By.CSS_SELECTOR, ".autocomplete-item")

    # Чекбоксы
    FREE_SHIPPING_CHECKBOX = (By.CSS_SELECTOR, "input#free-shipping")
    IN_STOCK_CHECKBOX = (By.CSS_SELECTOR, "input#in-stock")

    # ==================== Основные методы поиска ====================

    def search(self, query: str, press_enter: bool = False) -> None:
        """
        Выполнение поиска

        Args:
            query: поисковый запрос
            press_enter: если True, нажать Enter вместо кнопки поиска
        """
        with allure.step(f"Поиск по запросу: '{query}'"):
            search_input = self.wait_for_clickable(self.SEARCH_INPUT)
            self.highlight_element(search_input)
            search_input.clear()
            search_input.send_keys(query)

            if press_enter:
                search_input.send_keys(Keys.ENTER)
                self.logger.info(f"Search executed with Enter key: {query}")
            else:
                self.click(self.SEARCH_BUTTON)
                self.logger.info(f"Search executed with button click: {query}")

            # Ожидаем загрузки результатов
            self.wait_for_search_results()

    # def search_with_autocomplete(self, query: str, suggestion_index: int = 0) -> None:
    #     """
    #     Поиск с использованием автодополнения
    #
    #     Args:
    #         query: поисковый запрос
    #         suggestion_index: индекс предложения автодополнения
    #     """
    #     with allure.step(f"Поиск с автодополнением: '{query}'"):
    #         search_input = self.wait_for_clickable(self.SEARCH_INPUT)
    #         search_input.clear()
    #         search_input.send_keys(query)
    #
    #         # Ожидаем появление подсказок
    #         self.wait_for_visible(self.AUTOCOMPLETE_SUGGESTIONS)
    #         suggestions = self.find_elements(self.AUTOCOMPLETE_ITEM)
    #
    #         if suggestions and suggestion_index < len(suggestions):
    #             suggestions[suggestion_index].click()
    #             self.logger.info(f"Selected autocomplete suggestion at index {suggestion_index}")
    #             self.wait_for_search_results()

    # def advanced_search(self, **kwargs) -> None:
    #     """
    #     Расширенный поиск с фильтрами
    #
    #     Args:
    #         **kwargs: параметры поиска
    #             - query: поисковый запрос
    #             - category: категория
    #             - min_price: минимальная цена
    #             - max_price: максимальная цена
    #             - min_rating: минимальный рейтинг
    #             - free_shipping: бесплатная доставка
    #             - in_stock: в наличии
    #     """
    #     with allure.step("Расширенный поиск"):
    #         if 'query' in kwargs:
    #             self.search(kwargs['query'])
    #
    #         if 'category' in kwargs:
    #             self.select_category(kwargs['category'])
    #
    #         if 'min_price' in kwargs and 'max_price' in kwargs:
    #             self.set_price_range(kwargs['min_price'], kwargs['max_price'])
    #
    #         if 'min_rating' in kwargs:
    #             self.set_min_rating(kwargs['min_rating'])
    #
    #         if kwargs.get('free_shipping', False):
    #             self.select_free_shipping()
    #
    #         if kwargs.get('in_stock', False):
    #             self.select_in_stock()
    #
    #         self.apply_filters()

    # ==================== Методы работы с результатами ====================

    def wait_for_search_results(self, timeout: int = 10) -> None:
        """
        Ожидание загрузки результатов поиска

        Args:
            timeout: время ожидания в секундах
        """
        try:
            self.wait_for_invisible(self.LOADING_INDICATOR, timeout)
            self.wait_for_element(self.SEARCH_RESULTS, timeout)
            self.logger.info("Search results loaded")
        except:
            self.logger.warning("No search results found or timeout occurred")

    def get_search_results_count(self) -> int:
        """
        Получение количества результатов поиска

        Returns:
            int: количество найденных результатов
        """
        results = self.find_elements(self.SEARCH_RESULTS)
        count = len(results)
        self.logger.info(f"Found {count} search results")
        return count

    # def get_search_results_titles(self) -> List[str]:
    #     """
    #     Получение заголовков результатов поиска
    #
    #     Returns:
    #         List[str]: список заголовков
    #     """
    #     titles_elements = self.find_elements(self.SEARCH_RESULT_TITLES)
    #     titles = [elem.text for elem in titles_elements]
    #     self.logger.info(f"Retrieved {len(titles)} result titles")
    #     return titles
    #
    # def get_search_results_data(self) -> List[Dict[str, str]]:
    #     """
    #     Получение полных данных результатов поиска
    #
    #     Returns:
    #         List[Dict[str, str]]: список словарей с данными результатов
    #     """
    #     results = self.find_elements(self.SEARCH_RESULTS)
    #     data = []
    #
    #     for result in results:
    #         try:
    #             title = result.find_element(By.CSS_SELECTOR, ".title").text
    #             description = result.find_element(By.CSS_SELECTOR, ".description").text
    #             link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    #
    #             data.append({
    #                 "title": title,
    #                 "description": description,
    #                 "link": link
    #             })
    #         except:
    #             self.logger.warning(f"Failed to extract data from result element")
    #             continue
    #
    #     return data
    #
    # def click_on_result_by_index(self, index: int) -> None:
    #     """
    #     Клик по результату поиска по индексу
    #
    #     Args:
    #         index: индекс результата (начиная с 0)
    #     """
    #     results = self.find_elements(self.SEARCH_RESULTS)
    #     if index < len(results):
    #         self.highlight_element(results[index])
    #         results[index].click()
    #         self.logger.info(f"Clicked on search result at index {index}")
    #     else:
    #         raise IndexError(f"Result index {index} out of range. Total results: {len(results)}")

    def click_on_result_by_title(self, title: str) -> None:
        """
        Клик по результату поиска по заголовку

        Args:
            title: заголовок результата
        """
        titles = self.find_elements(self.SEARCH_RESULT_TITLES)
        for idx, title_element in enumerate(titles):
            if title_element.text == title:
                self.click_on_result_by_index(idx)
                self.logger.info(f"Clicked on result with title: {title}")
                return

        raise ValueError(f"No result found with title: {title}")

    # def get_search_summary(self) -> str:
    #     """
    #     Получение сводки поиска (количество результатов, время и т.д.)
    #
    #     Returns:
    #         str: текст сводки поиска
    #     """
    #     summary = self.get_text(self.SEARCH_SUMMARY)
    #     self.logger.info(f"Search summary: {summary}")
    #     return summary

    # def is_no_results_message_displayed(self) -> bool:
    #     """
    #     Проверка отображения сообщения об отсутствии результатов
    #
    #     Returns:
    #         bool: True если сообщение отображается
    #     """
    #     return self.is_element_visible(self.NO_RESULTS_MESSAGE, timeout=2)
    #
    # def get_no_results_message(self) -> str:
    #     """
    #     Получение текста сообщения об отсутствии результатов
    #
    #     Returns:
    #         str: текст сообщения
    #     """
    #     return self.get_text(self.NO_RESULTS_MESSAGE)

    # ==================== Методы работы с фильтрами ====================

    def select_category(self, category: str) -> None:
        """
        Выбор категории

        Args:
            category: название категории
        """
        category_locator = (By.XPATH, f"//label[contains(text(), '{category}')]")
        self.click(category_locator)
        self.logger.info(f"Selected category: {category}")

    # def set_price_range(self, min_price: int, max_price: int) -> None:
    #     """
    #     Установка диапазона цен
    #
    #     Args:
    #         min_price: минимальная цена
    #         max_price: максимальная цена
    #     """
    #     min_price_input = (By.CSS_SELECTOR, "input#min-price")
    #     max_price_input = (By.CSS_SELECTOR, "input#max-price")
    #
    #     self.input_text(min_price_input, str(min_price))
    #     self.input_text(max_price_input, str(max_price))
    #     self.logger.info(f"Set price range: {min_price} - {max_price}")
    #
    # def set_min_rating(self, rating: int) -> None:
    #     """
    #     Установка минимального рейтинга
    #
    #     Args:
    #         rating: рейтинг (1-5)
    #     """
    #     rating_locator = (By.XPATH, f"//div[@class='rating-filter']//span[@data-rating='{rating}']")
    #     self.click(rating_locator)
    #     self.logger.info(f"Set minimum rating: {rating}")
    #
    # def select_free_shipping(self) -> None:
    #     """Выбор фильтра бесплатной доставки"""
    #     self.click(self.FREE_SHIPPING_CHECKBOX)
    #     self.logger.info("Selected free shipping filter")
    #
    # def select_in_stock(self) -> None:
    #     """Выбор фильтра товаров в наличии"""
    #     self.click(self.IN_STOCK_CHECKBOX)
    #     self.logger.info("Selected in stock filter")
    #
    # def apply_filters(self) -> None:
    #     """Применение выбранных фильтров"""
    #     self.click(self.APPLY_FILTERS_BUTTON)
    #     self.wait_for_search_results()
    #     self.logger.info("Applied filters")
    #
    # def clear_filters(self) -> None:
    #     """Очистка всех фильтров"""
    #     self.click(self.CLEAR_FILTERS_BUTTON)
    #     self.wait_for_search_results()
    #     self.logger.info("Cleared all filters")
    #
    # # ==================== Методы работы с сортировкой ====================
    #
    # def sort_by_relevance(self) -> None:
    #     """Сортировка по релевантности"""
    #     self.select_sort_option(self.SORT_BY_RELEVANCE)
    #     self.logger.info("Sorted by relevance")
    #
    # def sort_by_price_asc(self) -> None:
    #     """Сортировка по возрастанию цены"""
    #     self.select_sort_option(self.SORT_BY_PRICE_ASC)
    #     self.logger.info("Sorted by price ascending")
    #
    # def sort_by_price_desc(self) -> None:
    #     """Сортировка по убыванию цены"""
    #     self.select_sort_option(self.SORT_BY_PRICE_DESC)
    #     self.logger.info("Sorted by price descending")
    #
    # def sort_by_rating(self) -> None:
    #     """Сортировка по рейтингу"""
    #     self.select_sort_option(self.SORT_BY_RATING)
    #     self.logger.info("Sorted by rating")
    #
    # def select_sort_option(self, option_locator: tuple) -> None:
    #     """
    #     Выбор опции сортировки
    #
    #     Args:
    #         option_locator: локатор опции сортировки
    #     """
    #     self.click(self.SORT_DROPDOWN)
    #     self.click(option_locator)
    #     self.wait_for_search_results()
    #
    # def get_current_sort_order(self) -> str:
    #     """
    #     Получение текущего порядка сортировки
    #
    #     Returns:
    #         str: текущий порядок сортировки
    #     """
    #     current_sort = self.get_text(self.SORT_DROPDOWN)
    #     self.logger.info(f"Current sort order: {current_sort}")
    #     return current_sort
    #
    # # ==================== Методы работы с пагинацией ====================
    #
    # def go_to_next_page(self) -> None:
    #     """Переход на следующую страницу"""
    #     if self.is_next_page_available():
    #         self.click(self.PAGINATION_NEXT)
    #         self.wait_for_search_results()
    #         self.logger.info("Navigated to next page")
    #
    # def go_to_previous_page(self) -> None:
    #     """Переход на предыдущую страницу"""
    #     if self.is_previous_page_available():
    #         self.click(self.PAGINATION_PREV)
    #         self.wait_for_search_results()
    #         self.logger.info("Navigated to previous page")

    def go_to_page(self, page_number: int) -> None:
        """
        Переход на конкретную страницу

        Args:
            page_number: номер страницы
        """
        page_locator = (By.XPATH, f"//div[@class='pagination']//a[text()='{page_number}']")
        self.click(page_locator)
        self.wait_for_search_results()
        self.logger.info(f"Navigated to page {page_number}")

    # def get_current_page_number(self) -> int:
    #     """
    #     Получение номера текущей страницы
    #
    #     Returns:
    #         int: номер текущей страницы
    #     """
    #     try:
    #         current_page_text = self.get_text(self.CURRENT_PAGE)
    #         page_number = int(current_page_text)
    #         return page_number
    #     except:
    #         return 1
    #
    # def get_total_pages_count(self) -> int:
    #     """
    #     Получение общего количества страниц
    #
    #     Returns:
    #         int: количество страниц
    #     """
    #     pages = self.find_elements(self.PAGINATION_PAGES)
    #     return len(pages)
    #
    # def is_next_page_available(self) -> bool:
    #     """
    #     Проверка наличия следующей страницы
    #
    #     Returns:
    #         bool: True если следующая страница доступна
    #     """
    #     return self.is_element_visible(self.PAGINATION_NEXT, timeout=2)
    #
    # def is_previous_page_available(self) -> bool:
    #     """
    #     Проверка наличия предыдущей страницы
    #
    #     Returns:
    #         bool: True если предыдущая страница доступна
    #     """
    #     return self.is_element_visible(self.PAGINATION_PREV, timeout=2)

    # ==================== Вспомогательные методы ====================

    # def get_autocomplete_suggestions(self) -> List[str]:
    #     """
    #     Получение подсказок автодополнения
    #
    #     Returns:
    #         List[str]: список подсказок
    #     """
    #     suggestions_elements = self.find_elements(self.AUTOCOMPLETE_ITEM)
    #     suggestions = [elem.text for elem in suggestions_elements]
    #     self.logger.info(f"Retrieved {len(suggestions)} autocomplete suggestions")
    #     return suggestions

    def clear_search(self) -> None:
        """Очистка поля поиска"""
        search_input = self.find_element(self.SEARCH_INPUT)
        search_input.clear()
        self.logger.info("Cleared search input")

    def get_search_query(self) -> str:
        """
        Получение текущего значения поля поиска

        Returns:
            str: значение поля поиска
        """
        query = self.get_attribute(self.SEARCH_INPUT, "value")
        self.logger.info(f"Current search query: {query}")
        return query

    def wait_for_autocomplete(self, timeout: int = 5) -> bool:
        """
        Ожидание появления автодополнения

        Args:
            timeout: время ожидания в секундах

        Returns:
            bool: True если автодополнение появилось
        """
        return self.is_element_visible(self.AUTOCOMPLETE_SUGGESTIONS, timeout)

    # def is_search_input_focused(self) -> bool:
    #     """
    #     Проверка, находится ли фокус на поле поиска
    #
    #     Returns:
    #         bool: True если поле поиска в фокусе
    #     """
    #     search_input = self.find_element(self.SEARCH_INPUT)
    #     is_focused = search_input == self.driver.switch_to.active_element
    #     return is_focused

    # ==================== Методы для проверок в тестах ====================

    # def verify_search_results_contain_text(self, text: str) -> bool:
    #     """
    #     Проверка, что результаты поиска содержат определенный текст
    #
    #     Args:
    #         text: искомый текст
    #
    #     Returns:
    #         bool: True если хотя бы один результат содержит текст
    #     """
    #     titles = self.get_search_results_titles()
    #     for title in titles:
    #         if text.lower() in title.lower():
    #             self.logger.info(f"Found text '{text}' in search results")
    #             return True
    #
    #     self.logger.warning(f"Text '{text}' not found in search results")
    #     return False
    #
    # def verify_all_results_contain_text(self, text: str) -> bool:
    #     """
    #     Проверка, что все результаты поиска содержат определенный текст
    #
    #     Args:
    #         text: искомый текст
    #
    #     Returns:
    #         bool: True если все результаты содержат текст
    #     """
    #     titles = self.get_search_results_titles()
    #     for title in titles:
    #         if text.lower() not in title.lower():
    #             self.logger.warning(f"Result '{title}' does not contain '{text}'")
    #             return False
    #
    #     self.logger.info(f"All {len(titles)} results contain text '{text}'")
    #     return True
    #
    # def verify_results_count(self, expected_count: int) -> bool:
    #     """
    #     Проверка количества результатов
    #
    #     Args:
    #         expected_count: ожидаемое количество
    #
    #     Returns:
    #         bool: True если количество совпадает
    #     """
    #     actual_count = self.get_search_results_count()
    #     is_match = actual_count == expected_count
    #     self.logger.info(f"Results count check: expected={expected_count}, actual={actual_count}, match={is_match}")
    #     return is_match
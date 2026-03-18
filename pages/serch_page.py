from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time

"""Класс, представляющий страницу поиска на Avito"""
class SearchPage:
    # Локаторы элементов
    JOB_SECTION_LINK = (By.XPATH, "#app > div > buyer-pages-mfe-location div.styles-singlePageWrapper-AYlq4 >"
                                  " div > div.index-center-J0kQo.index-center_withTitle-L0jpj.index-center_noMarginTop-C7KKK.index-centerWide-kehGi.index-centerDesign2023-iZwkS >"
                                  " div.index-outerPosition-dJhDy.index-outerPosition_rubricator-yizWk.index-outerPosition_main-yMQjs a:nth-child(3)") # Локатор кнопки "Работа"
    SEARCH_BUTTON = (By.XPATH, "//button[@aria-hidden='true'") # Локатор поля поиска "Все вакансии"
    SEARCH_INPUT = (By.XPATH, '//div[@class = "top-rubricator-tooltipIcon-EmmPK"]') # Локатор кноки "Найти"
    VACANCY_TITLES = (By.XPATH, '//h1[@class="page-title-text-Ihjnw page-title-inline-w6Beq"]') # Локатор заголовка вакансий
    COOKIE_ACCEPT_BUTTON = (By.XPATH, '//button[@class="_8761af61d40d8964 f6eebfeb30fe503c _534bd73718c723f4"]') # Локатор кнопки принятия cookie
    LOADER = (By.XPATH, "") # Локатор индикатора загрузки

# Конструктор __init__ создает объект ожидания 10с
def __init__(self, driver):
    self.driver = driver
    self.wait = WebDriverWait(self.driver, 10)

# Метод "open" открывает указанный URL и сразу обрабатывает cookie-баннер
def open(self, url):
    self.driver.get(url)
    print(f"Открыта страница: {url}")
    self.hfndle_cookies()

# Метод "handle_cookies" находит и кликает по кнопке "принять cookie" или игнорирует
def handle_cookies(self):
    try:
        cookie_button = self.wait.until(
            EC.element_to_be_clickable(self.COOKIE_ACCEPT_BUTTON),
            timeout=5)
        cookie_button.click()
        print("Cookie-банер принят")
        time.sleep(1)  #Дополнительное время для полной загрузки
    except TimeoutException:
        print("Cookie-банер не принят")

# Метод "go_to_job_section" переходит в раздел "Работа". Если ссылки нет - значит уже в раделе
def go_to_job_section(self):
    try:
        job_link = self.wait.until(
            EC.element_to_be_clickable(self.JOB_SECTION_LINK),
        )
        job_link.click()
        print("Перешли в раздел 'Раота'")
        time.sleep(2)  #Дополнительное время для полной загрузки
    except TimeoutException:
        print("Сылка на раздел 'Работа' не найдена, возможно уже в раделе")

# Метод "search" - основной метод поиска. Ождает поле, очищает, вводит, отправлет, идает результат
def search(self, query):
    try:
        search_input = self.wait.until(
            EC.presence_of_element_located((self.SEARCH_INPUT))
        )
        search_input.clear()
        search_input.send_keys(query)
        print (f"Введен поисковый запрос: {query}")
        time.sleep(1)  #Дополнительное время для полной загрузки
        search_input.submit()
        print("Поиск выполнен")
        self.wait_for_result()
    except Exception as e:
        print(f"Ошибка при поиске: {e}")
        raise

# Метод "wait_for_results" ожидает загузки результатов
def wait_for_results(self, timeout=10):
    # Ждем, пока исчезнет лоадер (если есть)
    try:
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located((self.LOADER))
        )
    except:
        pass
    # Ждем появления хотя бы оного элемента вакансии или сообщения об отсутствии результатов
    try:
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((self.VACANCY_TITLES+self.NO_RESULTS_MESSAGE))
        )
        print("Результты поиска заружены")
        time.sleep(2) #Дополнительое время для полной загрузки
    except TimeoutException:
        print("Время ожидания результатов истекло")

# Метод "get_vacancy_titles" получаетсписокзагловков вкансий
def get_vacancy_titles(self):
    try:
        # Ищем все заголовки вакансий
        title_element = self.driver.find_element(*self.VACANCY_TITLES)
        titles = [elem.text.strip() for elem in title_element if elem.text.strip()]
        # Фильтруем пустые строки
        titles = [t for t in titles if t]

        print(f"Найдено вакансий: {len(titles)}")
        if titles:
            print(f"Первые 3 вакансии: {titles[:3]}")
        return titles
    except Exception as e:
        print(f"Ошибка при получни заголовка: {e}")
        return []

# Метод "are_vacancies_found" проверяет результаты поиска
def are_vacancies_found(self):
    titles = self.get_vacancy_titles()
    if len(titles) > 0:
        print("Вкансии найдены")
        return True
    else:
        # Проверяем, нет ли сообщения об отсутствии результатов
        try:
            no_results = self.driver.find_element(*self.NO_RESULTS_MESSAGE)
            print(f"Вакансии не найдены: {no_results.text}")
            return False
        except:
            print("Вакансии не найдены, ет сообения об ошибке")
            return False

# Метод "check_vacancy_titles_contain" проверяет наличие ключевых слов в заголовках
def check_vacancy_titles_contain(self, keyword):
    titles = self.get_vacancy_titles()
    if not titles:
        return False, []
    # Приводим ключевое слово к нижнему регистру для сравнения
    keyword_lower = keyword.lower()
    # Проверяем каждую вакансию
    invalid_titles = []
    for title in titles:
        if keyword_lower not in title.lower():
            invalid_titles.append(title)
    if invalid_titles:
        print(f"Найдены вакансии без слова '{keyword}':")
        for t in invalid_titles[:5]:
            print(f"   - {t}")
        return False, invalid_titles
    else:
        print(f"Все вакансии содержат слово '{keyword}'")
        return True, []

# Метод "take_screenshot" делает скриншот текущего состояния страницы для отладки
def take_screenshot(self, filename="screenshot.png"):
    self.driver.save_screenshot(filename)
    print(f"Скриншот сохранен: {filename}")
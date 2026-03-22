from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException

class SearchPage(BasePage):
    # Локаторы элементов
    JOB_SECTION_LINK = (By.XPATH, '//img[@alt="Работа"]')
    # JOB_SECTION_LINK = (By.CSS_SELECTOR, "#app > div > buyer-pages-mfe-location div.styles-singlePageWrapper-AYlq4 > div > div.index-center-J0kQo.index-center_withTitle-L0jpj.index-center_noMarginTop-C7KKK.index-centerWide-kehGi.index-centerDesign2023-iZwkS > div.index-outerPosition-dJhDy.index-outerPosition_rubricator-yizWk.index-outerPosition_main-yMQjs a:nth-child(3)") # Локатор кнопки "Работа"
    SEARCH_BUTTON = (By.XPATH, "//button[@aria-hidden='true']") # Локатор поля поиска "Все вакансии"
    SEARCH_INPUT = (By.XPATH, '//div[@class = "top-rubricator-tooltipIcon-EmmPK"]') # Локатор кноки "Найти"
    VACANCY_TITLES = (By.XPATH, '//h1[@class="page-title-text-Ihjnw page-title-inline-w6Beq"]') # Локатор заголовка вакансий
    COOKIE_ACCEPT_BUTTON = (By.XPATH, '//button[@class="_8761af61d40d8964 f6eebfeb30fe503c _534bd73718c723f4"]') # Локатор кнопки принятия cookie

    def __init__(self, driver, url="https://www.avito.ru/perm/"):
        BasePage.__init__(self, driver, url)

    def accept_cookies(self):
        """Принять куки, если баннер отображается"""
        try:
            cookie_btn = self.driver.find_element(*self.COOKIE_ACCEPT_BUTTON)
            if cookie_btn.is_displayed():
                # Прокручиваем к кнопке и кликаем
                self.driver.execute_script("arguments[0].scrollIntoView(true);", cookie_btn)
                self.wait(1)
                cookie_btn.click()
                self.wait(1)
                return True
        except:
            pass  # Куки нет или уже приняты
        return False

    def click_job_section(self):
        """Клик по ссылке раздела 'Работа'"""
        # Принимаем куки
        self.accept_cookies()
        # Находим элемент
        element = self.driver.find_element(*self.JOB_SECTION_LINK)

        # Прокручиваем страницу к элементу
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        self.wait(1)  # Ждём завершения прокрутки

        try:
            element.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            # Если элемент перекрыт, используем JavaScript-клик
            self.driver.execute_script("arguments[0].click();", element)

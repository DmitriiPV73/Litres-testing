import time

class BasePage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        """Открывает страницу по заданному URL"""
        self.driver.get(self.url)

    def wait(self, seconds=5):
        """Простая задержка по времени (в секундах)"""
        time.sleep(seconds)




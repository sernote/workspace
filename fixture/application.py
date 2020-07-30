from selenium import webdriver
from appium import webdriver as mobile_driver

from fixture.log_service import Loghelper


class Application:
    """Test app"""
    def __init__(self):
        self.driver = None
        self.log = Loghelper(self)

    def destroy(self):
        """Destroying test session"""
        self.driver.quit()
        self.log.info('Ending tests')


class WebApplication(Application):
    """Web app"""
    def __init__(self):
        Application.__init__(self)
        self.driver = webdriver.Chrome()
        self.driver.set_page_load_timeout(10)
        self.driver.get("https://yandex.ru")
        self.log.info('Starting tests')

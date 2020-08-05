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
    def __init__(self, headless: bool = False):
        Application.__init__(self)
        opts = webdriver.ChromeOptions()
        if headless is True:
            opts.add_argument('headless')
            opts.add_argument('disable-gpu')
        self.driver = webdriver.Chrome(options=opts)
        self.driver.set_page_load_timeout(10)
        self.driver.get("https://yandex.ru")
        self.log.info('Starting tests')

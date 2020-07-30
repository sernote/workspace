from selenium import webdriver
from appium import webdriver as mobile_driver
import os


class Application:
    """Test app"""
    def __init__(self):
        self.driver = None

    def destroy(self):
        """Destroying test session"""
        self.driver.quit()


class WebApplication(Application):
    """Web app"""
    def __init__(self):
        Application.__init__(self)
        self.driver = webdriver.Chrome()
        self.driver.set_page_load_timeout(10)
        self.driver.get("https://yandex.ru")

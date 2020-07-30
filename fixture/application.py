from selenium import webdriver
from appium import webdriver as mobile_driver


class Application:
    """Test app"""
    def __init__(self):
        self.wd = None

    def destroy(self):
        """Destroying test session"""
        self.wd.quit()

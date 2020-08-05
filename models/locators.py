from selenium.webdriver.common.by import By


class BaseLocator:
    """Implement locator for page element"""
    def __init__(self, locator_value: str, locator_type=By.XPATH,  parent=None):
        self.locator_type = locator_type
        self.locator_value = locator_value
        self.parent = parent

    def __repr__(self):
        return "%s:%s:%s" % (self.__class__, self.locator_type, self.locator_value)

    def generate_xpath(self):
        raise NotImplementedError


class WebLocator(BaseLocator):
    def __init__(self, locator_value, locator_type, parent=None):
        BaseLocator.__init__(self, locator_value, locator_type, parent)

    def generate_xpath(self):
        if self.locator_type is By.XPATH:
            return self.locator_value
        elif self.locator_type is By.ID:
            return f'//*[contains(@id, "{self.locator_value}")]'
        else:
            raise NotImplementedError

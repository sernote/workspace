from models.pages.base_page import BasePage


class Element:
    """Implement page element and actions with it"""
    def __init__(self, page: BasePage, name: str, locators: list = None):
        self.page = page
        self.name = f'"{name}"'
        self.locators = locators
        self.app = page.app
        self.wait_timeout = self.page.wait_timeout

    def __repr__(self):
        return "%s:%s:%s" % (self.__class__, self.name, self.locators)


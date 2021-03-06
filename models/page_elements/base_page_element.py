from models.pages.base_page import BasePage

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import exceptions


class Element:
    """Implement page element and actions with it"""
    def __init__(self, page: BasePage, name: str, locators: list = None):
        self.page = page
        self.name = f'"{name}"'
        self.locators = self.check_for_parents_locators(locators)
        self.app = page.app
        self.wait_timeout = self.page.wait_timeout

    def __repr__(self):
        return "%s:%s:%s" % (self.__class__, self.name, self.locators)

    @staticmethod
    def check_for_parents_locators(locators: list) -> list:
        """Check locators for parents and build extended one"""
        for locator in locators:
            if locator.parent is not None:
                children_locators_list = locator.parent.generate_children_locators(locator)
                locators.remove(locator)
                locators.extend(children_locators_list)
        return locators

    def generate_children_locators(self, children_locator):
        """Create list of locators using xpath and all current type locators"""
        # TODO make smart locator type check
        target_locator_type = type(self.locators[0])  # this element always created thats why we can use first locator
        result_locators_list = []
        children_locator_xpath = children_locator.generate_xpath()
        for parent_locator in self.locators:
            if type(children_locator) is target_locator_type:
                children_locator.locator_value = parent_locator.generate_xpath() + children_locator_xpath
                children_locator.parent = None
                result_locators_list.append(children_locator)
        return result_locators_list

    def find_element(self, required_visibility=True) -> WebElement:
        """Find element by its locators list"""
        try:
            if required_visibility is True:
                result_element = self.wait_for_visibility_of_any(self.locators)
            else:
                # TODO presense_of_any
                raise NotImplementedError
        except exceptions.TimeoutException:
            self.app.log.error(
                f'Element {self.name} not found for {self.wait_timeout} sec. Locators: {str(self.locators)}')
            raise exceptions.TimeoutException
        else:
            return result_element

    def wait_for_visibility_of_any(self, locators: list, wait_timeout: int = None) -> WebElement:
        """Waiting for element be visible, or raise exception"""
        wd = self.app.driver
        if wait_timeout is None:
            wait_timeout = self.wait_timeout
        result = WebDriverWait(wd, wait_timeout, poll_frequency=0.1).until(
                VisibilityOfOneFromAny([(x.locator_type, x.locator_value) for x in locators]))
        return result

    def is_element_on_page(self, wait_timeout: int = None) -> bool:
        """Checking visibility status of element"""
        if wait_timeout is None:
            wait_timeout = self.wait_timeout
        self.app.log.info(f'Checking for elements visibility {self.name},page:{self.page.name}, time:{wait_timeout} s.')
        try:
            self.wait_for_visibility_of_any(self.locators, wait_timeout=wait_timeout)
        except exceptions.TimeoutException:
            self.app.log.info('Element not visible')
            return False
        else:
            self.app.log.info('Element is visible')
            return True

    def wait_for_element(self, wait_timeout: int = None, required_visibility: bool = True) -> WebElement:
        """Waiting for element"""
        if wait_timeout is None:
            wait_timeout = self.wait_timeout
        self.app.log.info(f'Waiting for element {self.name}, page: {self.page.name}')
        try:
            if required_visibility is True:
                element = self.wait_for_visibility_of_any(self.locators, wait_timeout)
            else:
                # TODO presense_of_any
                raise NotImplementedError
        except exceptions.TimeoutException:
            self.app.log.error(
                f'Element {self.name} not found,page: {self.page.name}, time:{wait_timeout} sec.'
                f' Locators:{self.locators}')
            raise exceptions.TimeoutException
        else:
            return element

    def click(self, required_visibility=True) -> WebElement:
        """Find and click on element"""
        result_element = self.wait_for_element(required_visibility=required_visibility, wait_timeout=5)
        self.app.log.info(f'Clicking on element: {self.name}, page: {self.page.name}')
        result_element.click()
        return result_element

    def clear_field(self) -> WebElement:
        """Find and clearing element(field)"""
        result_element = self.find_element()
        self.app.log.info(f'Clearing text in: {self.name}, page: {self.page.name}')
        result_element.clear()
        return result_element

    def input_text(self, text) -> WebElement:
        """Find and input text on element"""
        result_element = self.wait_for_element(wait_timeout=5)
        self.app.log.info(f'Sending text in: {self.name}, text: "{text}"')
        result_element.click()
        result_element.clear()
        result_element.send_keys(text)
        return result_element


class VisibilityOfOneFromAny(object):
    """Implement EC visibility_of_any for multi-locators"""
    def __init__(self, locators):
        self.locators = locators

    def __call__(self, driver):
        for locator in self.locators:
            try:
                element = driver.find_element(*locator)
                if element.is_displayed():
                    return element
                else:
                    return False
            except Exception:
                continue

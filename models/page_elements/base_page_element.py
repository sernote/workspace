from models.pages.base_page import BasePage


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

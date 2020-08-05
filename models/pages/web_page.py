from models.pages.base_page import BasePage


class WebPage(BasePage):
    def __init__(self, app, name):
        BasePage.__init__(self, app, name)
        self.wait_timeout = 10


class MainPage(WebPage):
    def __init__(self, app):
        WebPage.__init__(self, app, "Main web page")
        self.title_text = "main page title"
        self.sub_url = "/main_app/"
        self.main_search_field = NotImplemented

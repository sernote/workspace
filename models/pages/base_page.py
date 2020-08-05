from fixture.application import Application

from selenium.common import exceptions


class BasePage:
    """Page object, implements page and items on it"""
    def __init__(self, app: Application, name: str):
        self.app = app
        self.name = name
        self.title_text = None
        self.window = None  # window_handle
        self.wait_timeout = 1  # basic timeout for waiting elements on page
        self.window_anchor = None  # by this element we can identify page
        self.sub_url = None  # by this part of url we can identify page

    def __repr__(self):
        return "%s:%s:%s" % (self.__class__, self.name, self.window)

    def go_to_page_window(self):
        """Switching to page window"""
        if self.window is not None:
            if self.window != self.app.driver.current_window_handle:
                try:
                    self.app.log.info(f'Switching to page window {self.name}')
                    self.app.driver.switch_to.window(self.window)
                except exceptions.NoSuchWindowException:
                    handles = self.app.driver.window_handles
                    self.app.log.error(f'No window "{self.window}" in windows handles list: {handles}')
                    raise exceptions.NoSuchWindowException
        else:
            if self.is_window_exist() is False:
                self.app.log.error(f'Unable to switch to the page "{self.name}"')
                raise NotImplementedError

    def is_window_exist(self) -> bool:
        """Finding windows handler by anchor, title, url"""
        self.app.log.info(f"Checking the page exists {self.name}")
        windows = self.app.driver.window_handles
        for window in windows:
            try:
                self.app.driver.switch_to.window(window)
                if self.window_anchor is not None:
                    raise NotImplementedError
                elif self.title_text is not None and self.title_text in self.app.driver.title:
                    self.window = window
                    self.app.log.info('Window handle found by title')
                    break
                elif self.sub_url is not None and self.sub_url in self.app.driver.current_url:
                    self.window = window
                    self.app.log.info('Window handle found by url')
                    break
            except exceptions.NoSuchWindowException:
                self.app.log.info('Some window was closed. Mb its missing notify')
        if self.window is None:
            self.app.log.info('Unable to find window handler')
            return False
        else:
            return True

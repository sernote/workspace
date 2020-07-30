import logging

logging.basicConfig(filename='log.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class Loghelper:
    def __init__(self, app):
        self.app = app
        self.debuglog = logging

    def info(self, text: str):
        self.debuglog.info(text)

import logging

logging.basicConfig(filename='log.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class Loghelper:
    """Logger"""
    def __init__(self, app):
        self.app = app
        self.debuglog = logging

    def info(self, text: str):
        """Add info log"""
        self.debuglog.info(text)

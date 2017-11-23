import logging

from config.Config import Config


class LocalLogger:

    def __init__(self):
        self.config = Config()

    def get_logger(self):
        return logging.getLogger(__name__)
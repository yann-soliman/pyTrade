from config.Config import Config


class Logger:

    def __init__(self):
        self.config = Config()

    def get_logger(self):
        return self.config.get_logger()
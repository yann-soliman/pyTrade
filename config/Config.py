import os

from config.HerokuConfig import HerokuConfig
from config.LocalConfig import LocalConfig


class Config:
    def __init__(self):
        if os.environ.get('HEROKU_APP') == "true":
            self.config = HerokuConfig()
        else:
            self.config = LocalConfig()

    def get_logger(self):
        return self.config.get_logger()

    def get_storage(self):
        return self.config.get_storage()

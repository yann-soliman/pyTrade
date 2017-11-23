from config.Config import Config


class Storage:

    def __init__(self):
        self.config = Config()

    def get_storage(self):
        return self.config.get_storage()
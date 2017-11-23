import logging

from storage.MongoFileStorage import MongoFileStorage


class LocalConfig:
    def get_logger(self):
        return logging.getLogger(__name__)

    def get_storage(self):
        return MongoFileStorage()

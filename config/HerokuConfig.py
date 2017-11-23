import os

from logger.LogDNALogger import LogDNALogger
from storage.RedisStorage import RedisStorage


class HerokuConfig:
    def __init__(self):
        self.logdna_key = os.environ.get('LOGDNA_KEY')
        self.redis_url = os.environ.get('REDIS_URL')

    def get_logdna_key(self):
        return self.logdna_key

    def get_redis_url(self):
        return self.redis_url

    def get_logger(self):
        return LogDNALogger(self.logdna_key).get_logger()

    def get_storage(self):
        return RedisStorage(self.redis_url)
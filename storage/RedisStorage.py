import redis

from storage.AbstractStorage import AbstractStorage


class RedisStorage(AbstractStorage):
    def __init__(self, redis_url):
        self.redis = redis.from_url(redis_url)

    def upsert(self, key, value):
        self.redis.set(key, value)

    def get(self, key):
        self.redis.get(key)

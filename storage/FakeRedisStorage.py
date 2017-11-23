import fakeredis

from storage.AbstractStorage import AbstractStorage


class FakeRedisStorage(AbstractStorage):
    def __init__(self):
        self.redis = fakeredis.FakeStrictRedis()

    def upsert(self, key, value):
        self.redis.set(key, value)

    def get(self, key):
        self.redis.get(key)

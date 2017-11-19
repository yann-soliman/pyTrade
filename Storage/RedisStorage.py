import fakeredis


class RedisStorage:
    def __init__(self):
        self.redis = fakeredis.FakeStrictRedis()

    def set(self, key, value):
        self.redis.set(key, value)

    def get(self, key):
        self.redis.get(key)

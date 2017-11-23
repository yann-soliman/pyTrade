from tinydb import TinyDB, Query

from storage.AbstractStorage import AbstractStorage


class MongoFileStorage(AbstractStorage):
    def __init__(self):
        self.storage = TinyDB('db.json')

    def upsert(self, key, value):
        self.storage.upsert({"key": key, "value": value}, Query().key == key)

    def get(self, key):
        stored_object = self.storage.get(Query().key == key)
        if stored_object is None:
            return None
        return stored_object["value"]

from abc import ABC, abstractmethod


class AbstractStorage(ABC):

    @abstractmethod
    def upsert(self, key, value):
        pass

    @abstractmethod
    def get(self, key):
        pass
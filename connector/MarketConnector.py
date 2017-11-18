import copy
from abc import ABC, abstractmethod


class MarketConnector(ABC):
    @abstractmethod
    def get_best_bids_price(self, currency1, currency2):
        pass

    @abstractmethod
    def get_best_asks_price(self, currency1, currency2):
        pass

import gdax
import requests
from expiringdict import ExpiringDict

from connector.CoinMarketCapConnector import CoinMarketCapConnector
from connector.MarketConnector import MarketConnector


class BithumbApi:
    API_URL = "https://api.bithumb.com"

    def __init__(self):
        self.cache = ExpiringDict(max_len=100, max_age_seconds=30)

    def order_book(self, currency):
        if self.cache.get("orderbook-" + currency) is None:
            r = requests.get(self.API_URL + '/public/orderbook/{}'.format(currency))
            if r.status_code is 200:
                json = r.json()
                if json["status"] == "0000" :
                    self.cache["orderbook-" + currency] = json

        return self.cache.get("orderbook-" + currency)

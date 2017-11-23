from http.client import HTTPException

import krakenex
import time
from expiringdict import ExpiringDict

from connector.MarketConnector import MarketConnector
from logger.Logger import Logger


class KrakenConnector(MarketConnector):
    def __init__(self):
        self.cache = ExpiringDict(max_len=100, max_age_seconds=5)
        self.logger = Logger().get_logger()
        self.k = krakenex.API()

    def get_best_bids_price(self, currency1, currency2):
        pair = currency1 + currency2
        if self.cache.get(pair + "b") is None:
            ticker = self.get_ticker(currency1, currency2)
            if ticker is not None:
                self.cache[pair + "b"] = float(ticker['result'][pair]['b'][0])

        return self.cache.get(pair + "b")

    def get_best_asks_price(self, currency1, currency2):
        pair = currency1 + currency2
        return float(self.get_ticker(currency1, currency2)['result'][pair]['a'][0])

    def get_time(self):
        return self.k.query_public("Time")

    def get_assets(self):
        return self.k.query_public("Assets")

    def get_asset_pairs(self):
        return self.k.query_public("AssetPairs")

    def get_ticker(self, currency1, currency2):
        data = {'pair': currency1 + currency2}
        return self._query_public("Ticker", data)

    def _query_public(self, method, data=None):
        try:
            def func():
                return self.k.query_public(method, data)

            return self._multiple_tries(func, 3)
        except Exception as e:
            self.logger.error("Erreur lors de l'appel à krakik...")

    def _multiple_tries(self, func, times):
        for _ in range(times):
            try:
                return func()
            except HTTPException as e:
                self.logger.error("got exception with HTTP code : %s", e.args[0])
                self.k.conn.close()
                time.sleep(1)
        raise Exception('Tried to call krakik %s times without success', times)

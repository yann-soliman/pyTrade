import gdax

from api.BithumbApi import BithumbApi
from connector.CoinMarketCapConnector import CoinMarketCapConnector
from connector.MarketConnector import MarketConnector


class BithumbConnector(MarketConnector):
    def __init__(self):
        self.api = BithumbApi()

    def get_best_bids_price(self, currency1, currency2):
        order_book = self.api.order_book(currency1)
        if order_book is not None:
            data = self.api.order_book(currency1)["data"]
            average_bid = 0
            for index, bid in enumerate(data["bids"]):
                average_bid = (float(bid["price"]) + average_bid * index) / (index+1)
            return self.convert_currency(average_bid, data["payment_currency"], currency2)
        return None

    def get_best_asks_price(self, currency1, currency2):
        return self.api.order_book(currency1)

    def convert_currency(self, amount, currency1, currency2):
        # TODO : sortir dans un module séparé et appelé une API qui fait la conversion
        if currency1 == "KRW" and currency2 == "EUR":
            return amount * 0.0007791265474552958

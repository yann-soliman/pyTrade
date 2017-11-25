import gdax

from connector.MarketConnector import MarketConnector


class GdaxConnector(MarketConnector):
    def __init__(self):
        self.public_client = gdax.PublicClient()

    def get_best_bids_price(self, currency1, currency2):
        return float(self.public_client.get_product_order_book(currency1 + "-" + currency2)['bids'][0][0])

    def get_best_asks_price(self, currency1, currency2):
        return float(self.public_client.get_product_order_book(currency1 + "-" + currency2)['asks'][0][0])

    def get_ticker(self, currency1, currency2):
        return self.public_client.get_product_ticker(currency1 + "-" + currency2)

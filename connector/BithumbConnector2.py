from connector.CoinMarketCapConnector import CoinMarketCapConnector
from connector.MarketConnector import MarketConnector


class BithumbConnector2(MarketConnector):
    def __init__(self):
        self.coin_market_cap_connector = CoinMarketCapConnector()

    def get_best_bids_price(self, currency1, currency2):
        return self.coin_market_cap_connector.get_average_markets_price(currency1, currency2)["Bithumb"]["price"]

    def get_best_asks_price(self, currency1, currency2):
        return self.coin_market_cap_connector.get_average_markets_price(currency1, currency2)["Bithumb"]

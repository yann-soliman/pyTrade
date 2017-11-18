from connector.BithumbConnector import BithumbConnector
from connector.GdaxConnector import GdaxConnector
from connector.KrakenConnector import KrakenConnector


class MarketComparator:
    def __init__(self):
        self.gdax = GdaxConnector()
        self.kraken = KrakenConnector()
        self.bithumb = BithumbConnector()

    def compare_bithumb_kraken(self, currency1, currency2):
        """
        Compare la différence de prix entre bithumb et kraken
        Retourne la différence entre les deux en %
        :param currency1: devise à échanger
        :param currency2: devise échangée
        :return: le pourcentage (positif ou négatif) de différence
        """
        price_bithumb = self.bithumb.get_best_bids_price(currency1, currency2)
        price_kraken = self.kraken.get_best_bids_price(currency1, currency2)

        if price_kraken is not None and price_bithumb is not None:
            if price_bithumb > price_kraken:
                return 100 - price_kraken / price_bithumb * 100
            else:
                return price_bithumb / price_kraken * 100 - 100
        return 0

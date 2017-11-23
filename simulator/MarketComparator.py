from connector.BithumbConnector import BithumbConnector
from connector.CryptoCompareConnector import CryptoCompareConnector
from connector.GdaxConnector import GdaxConnector
from connector.KrakenConnector import KrakenConnector
from logger.Logger import Logger


class MarketComparator:
    def __init__(self):
        self.logger = Logger().get_logger()
        self.gdax = GdaxConnector()
        self.kraken = KrakenConnector()
        self.bithumb = BithumbConnector()
        self.crypto_compare = CryptoCompareConnector()

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

    def compare_cryptocompare_kraken_in_euro(self, currency1):
        # TODO : méthode générique de comparaison...
        """
        Compare la différence de prix entre bithumb et kraken
        Retourne la différence entre les deux en %
        :param currency1: devise à échanger
        :param currency2: devise échangée
        :return: le pourcentage (positif ou négatif) de différence
        """

        price_bithumb = self.bithumb.get_best_bids_price(currency1, "EUR")
        price_crypto = self.crypto_compare.get_price_in_euro(currency1)
        price_kraken = self.kraken.get_best_bids_price(currency1, "EUR")

        if price_kraken is not None and price_crypto is not None and price_bithumb is not None:
            price_average_markets = (price_bithumb + price_crypto) / 2
            self.logger.info("Comparaison du prix kraken %s avec une moyenne de bithumb et cryptocompare %s", price_kraken, price_average_markets)
            if price_average_markets > price_kraken:
                percentage = 100 - price_kraken / price_average_markets * 100
                self.logger.info("%s %% de différence", percentage)
                return percentage
            else:
                percentage = price_average_markets / price_kraken * 100 - 100
                self.logger.info("%s %% de différence", percentage)
                return percentage
        return 0

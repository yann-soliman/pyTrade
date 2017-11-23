import time

from config.Config import Config
from logger.Logger import Logger
from alert.SoundAlert import SoundAlert
from connector.BithumbConnector import BithumbConnector
from connector.BithumbConnector2 import BithumbConnector2
from connector.CryptoCompareConnector import CryptoCompareConnector
from connector.KrakenConnector import KrakenConnector
from market.Market import Market
from model.money.BitcoinCash import BitcoinCash
from model.money.Euro import Euro
from simulator.MarketComparator import MarketComparator


class ComparatorSimulator:
    THRESHOLD = 1

    def __init__(self):
        self.marketComparator = MarketComparator()
        self.market = Market()
        self.bithumb = BithumbConnector()
        self.bithumb_coin_market = BithumbConnector2()
        self.kraken = KrakenConnector()
        self.crypto_compare = CryptoCompareConnector()
        self.alert = SoundAlert()
        self.logger = Logger().get_logger()

    def simulate(self):
        # On commence la simulation avec 1000 €
        if not self.market.has_money_in_wallet():
            self.market.add_euro_on_wallet(1000)

        while True:
            self.market.print_balance()
            bithum_price = self.bithumb.get_best_bids_price("BCH", "EUR")
            self.logger.info("bithumb : %s", bithum_price)
            crypto_compare = self.crypto_compare.get_price_in_euro("BCH")
            self.logger.info("crypto-compare : %s", crypto_compare)
            kraken_price = self.kraken.get_best_bids_price("BCH", "EUR")
            self.logger.info("kraken : %s", kraken_price)

            comparaison_percentage = self.marketComparator.compare_cryptocompare_kraken_in_euro("BCH")
            if comparaison_percentage > self.THRESHOLD and self.market.get_balance("EUR").amount > 0:
                self.alert.alert_buy()
                euro = Euro(kraken_price)
                self.market.buy_all("BCH", euro)
            elif comparaison_percentage < - self.THRESHOLD:
                self.alert.alert_sell()
                euro = Euro(kraken_price)
                self.market.sell_all("BCH", euro)
            time.sleep(5)

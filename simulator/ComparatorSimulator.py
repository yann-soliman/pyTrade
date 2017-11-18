import time

import winsound

from Market import Market
from MarketComparator import MarketComparator
from connector.BithumbConnector import BithumbConnector
from connector.BithumbConnector2 import BithumbConnector2
from connector.KrakenConnector import KrakenConnector
from model.money.BitcoinCash import BitcoinCash
from model.money.Euro import Euro


class ComparatorSimulator:
    THRESHOLD = 1

    def __init__(self):
        self.marketComparator = MarketComparator()
        self.market = Market()
        self.bithumb = BithumbConnector()
        self.bithumb_coin_market = BithumbConnector2()
        self.kraken = KrakenConnector()

    def simulate(self):
        self.market.add_euro_on_wallet(1000)

        while True:
            print("bithumb", self.bithumb.get_best_bids_price("BCH", "EUR"))
            print("bithumb@coinmarket", self.bithumb_coin_market.get_best_bids_price("BCH", "EUR"))
            kraken_price = self.kraken.get_best_bids_price("BCH", "EUR")
            print("kraken", kraken_price)
            if kraken_price is not None:
                if self.marketComparator.compare_bithumb_kraken("BCH", "EUR") > self.THRESHOLD and self.market.get_balance("EUR").amount > 0:
                    winsound.PlaySound('sounds/sound.wav', winsound.SND_FILENAME)
                    euro = Euro(kraken_price)
                    self.market.buy_all("BCH", euro)
                elif self.marketComparator.compare_bithumb_kraken("BCH", "EUR") < - self.THRESHOLD:
                    winsound.PlaySound('sounds/no.wav', winsound.SND_FILENAME)
                    bch = BitcoinCash(kraken_price)
                    self.market.sell_all("EUR", bch)
            time.sleep(2)

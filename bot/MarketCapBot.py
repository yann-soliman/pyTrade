from time import sleep

from alert.EmailAlert import EmailAlert
from connector.CoinMarketCapConnector import CoinMarketCapConnector


class MarketCapBot:
    THRESHOLD = 1

    def __init__(self):
        self.alert = EmailAlert()
        self.coinmarket_cap_connector = CoinMarketCapConnector()
        self.me = "yann.soliman@gmail.com"
        self.mf = "tom_lyo@hotmail.fr"

    def run(self):
        previous_cap = 404696353544.65

        while True:
            cap = self.coinmarket_cap_connector.get_market_cap()
            if previous_cap is not None and abs((previous_cap - cap) / previous_cap * 100) >= self.THRESHOLD:
                message = "ALERTE, coinmarket cap avant : " + str(previous_cap) + " et maintenant : " + str(cap)
                self.alert.send_message(self.me, message)
                self.alert.send_message(self.mf, message)
                print("ALERTE, coinmarket cap avant : " + str(previous_cap) + " et maintenant : " + str(cap))
            previous_cap = cap
            sleep(10)

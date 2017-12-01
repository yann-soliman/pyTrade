from time import sleep

from alert.EmailAlert import EmailAlert
from connector.CoinMarketCapConnector import CoinMarketCapConnector


class MarketCapBot:
    THRESHOLD = 0.8

    def __init__(self):
        self.alert = EmailAlert()
        self.coinmarket_cap_connector = CoinMarketCapConnector()
        self.me = "yann.soliman@gmail.com"
        self.mf = "tom_lyo@hotmail.fr"
        self.matt = "langlois.matt@gmail.com"

    def run(self):
        previous_cap = 99999999999

        while True:
            cap = self.coinmarket_cap_connector.get_market_cap()
            if abs((previous_cap - cap) / previous_cap * 100) >= self.THRESHOLD:
                message = "ALERTE, coinmarket cap avant : " + str(previous_cap) + " et maintenant : " + str(cap)
                self.alert.send_message(self.me, message)
                self.alert.send_message(self.mf, message)
                self.alert.send_message(self.matt, message)
                print("ALERTE, coinmarket cap avant : " + str(previous_cap) + " et maintenant : " + str(cap))
            previous_cap = cap
            sleep(10)

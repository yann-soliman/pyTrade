import time

from alert.SoundAlert import SoundAlert
from connector.GdaxConnector import GdaxConnector
from logger.Logger import Logger
from market.Market import Market
from model.money.Euro import Euro
from utils.MoneyDeserializer import MoneyDeserializer


class GdaxCompulsifSimulator:
    """
    Simulator d'achat dit compulsif sur GDAX.
    La stratégie est d'acheter palier par palier dès que le prix descend et de poser directement un ordre de vente à MARGIN% plus cher
    Puisque les fees sont de 0 pour les makers, on devrait pas trop mal s'en sortir
    """

    # Marge en pourcentage à laquelle revendre le coin qui a été acheté
    MARGIN = 1
    # Montant en € acheté à chaque palier
    STEP_DIFFERENCE = 100
    # Palier en € pour lequel acheter
    BUYING_STEP = 1

    def __init__(self, currency):
        self.market = Market()
        self.alert = SoundAlert()
        self.logger = Logger().get_logger()
        self.gdax = GdaxConnector()
        # Montant du dernier achat
        self.last_buying_price = 1000
        self.currency = currency

        # Variables pour la simulation du market
        self.last_trade_id = None
        self.selling_orders = {}

    def simulate(self):

        # On commence la simulation avec 1000 €
        if not self.market.has_money_in_wallet():
            self.market.add_euro_on_wallet(1000)

        self.market.print_balance()

        while True:
            ticker = self.gdax.get_ticker(self.currency, "EUR")
            print(ticker)
            if ticker is not None:
                ask_price = float(ticker['ask'])
                if self.should_buy(ask_price) and self.market.get_balance("EUR").amount > 0.1:
                    self.alert.alert_buy()
                    money_amount = MoneyDeserializer.deserialize(self.currency, self.STEP_DIFFERENCE / ask_price)
                    money_price = Euro(ask_price)
                    self.market.buy(money_amount, money_price)
                    self.last_buying_price = self.STEP_DIFFERENCE / ask_price
                    self.market.print_balance()
                    self.market.print_balance()

                self.do_market(ticker["trade_id"], float(ticker["price"]))
            time.sleep(5)

    def should_buy(self, ask_price):
        """
        Défini ce qui conditionne l'achat, toute l'intelligence est là
        :param ask_price:
        :return:
        """
        return ask_price > self.last_buying_price - self.BUYING_STEP

    def place_selling_order(self, buying_price):
        selling_price = (buying_price + self.MARGIN) / 100
        amount = self.STEP_DIFFERENCE / buying_price
        self.selling_orders[selling_price] = amount

    def do_market(self, trade_id, trade_price):
        """
        Simule ce que ferait le marcher dans ce cas
        Ne prend pas en compte la quantité vendue
        :return:
        """
        if self.last_trade_id != trade_id:
            for price, amount in self.selling_orders.items():
                if price >= trade_price:
                    self.alert.alert_sell()
                    money_amount = MoneyDeserializer.deserialize(self.currency, amount)
                    money_price = Euro(price)
                    self.market.sell(money_amount, money_price)
                    del self.selling_orders[price]
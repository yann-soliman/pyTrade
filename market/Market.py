import copy

from logger.Logger import Logger
from model.money.Euro import Euro
from utils.ExchangeRateCalculator import ExchangeRateCalculator
from utils.MoneyDeserializer import MoneyDeserializer
from wallet.Wallet import Wallet


class Market:
    def __init__(self):
        self.logger = Logger().get_logger()
        self.wallet = Wallet()

    def add_euro_on_wallet(self, amount):
        self.logger.info("[+] Ajout de %s euro dans le wallet", amount)
        self.wallet.plus(Euro(amount))

    def buy(self, money_amount, money_price):
        """
         Achète money_amount au prix de money_price l'unité
        :param money1: la Money à acheter
        :param money2: prix de la Money avec laquelle faire l'échange
        :return: void
        """
        if money_amount.amount <= 0:
            self.logger.error("Impossible d'acheter %s", money_amount)
            return
        if money_price.amount <= 0:
            self.logger.error("Impossible d'acheter %s car le prix d'achat est trop faible", money_amount)
            return

        # Conversion
        money_to_sell = ExchangeRateCalculator.convert(money_amount, money_price)

        # Si le wallet a assez de fond pour acheter
        if self.wallet.has_enough_funds(money_to_sell):
            self.logger.info("J'achète %s au prix de %s l'unité", money_amount, money_price)
            self.wallet.minus(money_to_sell)
            self.wallet.plus(money_amount)
        else:
            self.logger.error("Impossible d'acheter %s. Seulement %s disponible dans le wallet.", money_amount,
                              self.wallet.get_balance(money_price.currency))

    def buy_all(self, currency, money_price):
        """
        Dépense toute la thune possible du wallet pour acheter la devise au prix indiqué
        :param currency: devise à acheter
        :param money_price: prix pour une unité
        :return:
        """
        total_money_in_wallet = self.get_balance(money_price.currency)
        if total_money_in_wallet.amount > 0:
            # TODO : Quelle est la bonne façon d'instancier un Money à partir de sa devise ???
            money_to_buy = MoneyDeserializer.deserialize(currency)
            money_to_buy.amount = total_money_in_wallet.amount / money_price.amount
            self.buy(money_to_buy, money_price)
        else:
            self.logger.error("Fonds insufisant pour acheter.")

    def sell(self, money_amount, money_price):
        """
         Vend money_amount au prix de money_price l'unité
        :param money1: la Money à vendre
        :param money2: prix de la Money avec laquelle faire l'échange
        :return: void
        """
        if money_amount.amount <= 0:
            self.logger.error("Impossible de vendre %s", money_amount)
            return
        if money_price.amount <= 0:
            self.logger.error("Impossible de vendre %s car le prix d'achat est trop faible", money_amount)
            return
        # Si on a assez de fond de ce qu'on souhaite vendre dans le wallet
        if self.wallet.has_enough_funds(money_amount):
            self.logger.info("Je vends %s au prix de %s l'unité", money_amount, money_price)
            # Conversion
            money_to_buy = ExchangeRateCalculator.convert(money_amount, money_price)
            self.wallet.minus(money_amount)
            self.wallet.plus(money_to_buy)
        else:
            self.logger.error("Impossible de vendre %s . Seulement %s disponible dans le wallet.", money_amount,
                              self.wallet.get_balance(money_price.currency))

    def sell_all(self, currency, money_price):
        """
        Bazarde toutes les devises possibles du wallet pour vendre la devise au prix indiqué
        :param currency: devise à vendre
        :param money_price: prix pour une unité
        :return:
        """
        total_money_in_wallet = self.get_balance(currency)
        if total_money_in_wallet.amount > 0:
            self.sell(total_money_in_wallet, money_price)
        else:
            self.logger.warning("Rien à vendre.")

    def print_balance(self):
        self.wallet.print_balance()

    def get_balance(self, currency):
        return copy.copy(self.wallet.get_balance(currency))

    def has_money_in_wallet(self):
        return self.wallet.has_moneys()

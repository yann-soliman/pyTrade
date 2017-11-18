import copy
import logging

from ExchangeRateCalculator import ExchangeRateCalculator
from Wallet import Wallet
from model.money.BitcoinCash import BitcoinCash
from model.money.Euro import Euro
from model.money.Money import Money

logger = logging.getLogger(__name__)


class Market:
    def __init__(self):
        self.wallet = Wallet()

    def add_euro_on_wallet(self, amount):
        self.wallet.plus(Euro(amount))

    def buy(self, money_amount, money_price):
        """
         Achète money_amount au prix de money_price l'unité
        :param money1: la Money à acheter
        :param money2: prix de la Money avec laquelle faire l'échange
        :return: void
        """
        if money_amount.amount <= 0:
            print("[-] Impossible d'acheter", money_amount)
            return
        if money_price.amount <= 0:
            print("[-] Impossible d'acheter", money_amount, "car le prix d'achat est trop faible")
            return

        # Conversion
        money_to_sell = ExchangeRateCalculator.convert(money_amount, money_price)

        # Si le wallet a assez de fond pour acheter
        if self.wallet.has_enough_funds(money_to_sell):
            print("J'achète", money_amount, "au prix de", money_price, "l'unité")
            self.wallet.minus(money_to_sell)
            self.wallet.plus(money_amount)
        else:
            print("[-] Impossible d'acheter", money_amount, ". Seulement ",
                  self.wallet.get_balance(money_price.currency), "disponible dans le wallet.")

    def buy_all(self, currency, money_price):
        """
        Dépense toute la thune possible du wallet pour acheter la devise au prix indiqué
        :param currency: devise à acheter
        :param money_price: prix pour une unité
        :return:
        """
        total_money_in_wallet = self.get_balance(money_price.currency)
        if total_money_in_wallet.amount > 0:
            money_to_buy = Market.new_money_with_currency(currency)
            money_to_buy.amount = total_money_in_wallet.amount / money_price.amount
            self.buy(money_to_buy, money_price)
        else:
            print("[-] Fonds insufisant pour acheter.")

    def sell(self, money_amount, money_price):
        """
         Vend money_amount au prix de money_price l'unité
        :param money1: la Money à vendre
        :param money2: prix de la Money avec laquelle faire l'échange
        :return: void
        """
        if money_amount.amount <= 0:
            print("[-] Impossible de vendre", money_amount)
            return
        if money_price.amount <= 0:
            print("[-] Impossible de vendre", money_amount, "car le prix d'achat est trop faible")
            return
        # Si on a assez de fond de ce qu'on souhaite vendre dans le wallet
        if self.wallet.has_enough_funds(money_amount):
            print("Je vends", money_amount, "au prix de", money_price, "l'unité")
            # Conversion
            money_to_buy = ExchangeRateCalculator.convert(money_amount, money_price)
            self.wallet.minus(money_amount)
            self.wallet.plus(money_to_buy)
        else:
            print("[-] Impossible de vendre", money_amount, ". Seulement ",
                  self.wallet.get_balance(money_price.currency), money_price.currency, "disponible dans le wallet.")

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
            print("[-] Rien à vendre.")

    def print_balance(self):
        self.wallet.print_balance()

    def get_balance(self, currency):
        return copy.copy(self.wallet.get_balance(currency))

    @staticmethod
    def new_money_with_currency(currency):
        if currency == "BCH":
            return BitcoinCash()
        if currency == "EUR":
            return Euro()
            # ... todo ce truc dégeulasse ?

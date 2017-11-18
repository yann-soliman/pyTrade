import copy
import logging

import math

from model.money.Bitcoin import Bitcoin
from model.money.Euro import Euro
from model.money.Litcoin import Litcoin

from model.money.Ethereum import Ethereum

logger = logging.getLogger(__name__)


class Wallet:

    def __init__(self, initial_eur_balance=0):
        self._btc = Bitcoin(0)
        self._eur = Euro(initial_eur_balance)
        self._eth = Ethereum(0)
        self._ltc = Litcoin(0)

    def __operation_on_wallet(self, money):
        for money_in_wallet in self.get_money_list_in_wallet():
            if money.currency == money_in_wallet.currency:
                money_in_wallet.amount += money.amount

    def plus(self, money):
        self.__operation_on_wallet(money)

    def minus(self, money):
        money.amount = - money.amount
        self.__operation_on_wallet(money)

    def get_balance(self, currency):
        for money_in_wallet in self.get_money_list_in_wallet():
            if currency == money_in_wallet.currency:
                return copy.copy(money_in_wallet)

    def has_enough_funds(self, money):
        for money_in_wallet in self.get_money_list_in_wallet():
            if money.currency == money_in_wallet.currency:
                return money_in_wallet.amount >= money.amount or math.isclose(money_in_wallet.amount, money.amount )

    def get_money_list_in_wallet(self):
        return [self._eur, self._btc, self._eth, self._ltc]

    def print_balance(self):
        print("==============")
        for moneyInWallet in self.get_money_list_in_wallet():
            print(moneyInWallet)
        print("==============")



import copy
from abc import ABC


class Money(ABC):
    def __init__(self, amount=0):
        self.amount = float(amount)
        self.currency = ""

    def get_same_currency_money_with_amount(self, amount):
        """
        Retourne une Money avec la même devise et un montant de amount
        :return: Money
        """
        money = copy.copy(self)
        money.amount = amount
        return money


    @staticmethod
    def is_crypto_money(money):
        return money.currency == "BTC" or money.currency == "BCH" or money.currency == "ETH" or money.currency == "LTC"

    def __str__(self):
        return "[" + str(self.currency) + "] : " + str(self.amount)

    def __lt__(self, other):
        return self.amount < other.amount

    def ___le__(self, other):
        return self.amount <= other.amount

    def __eq__(self, other):
        return self.amount == other.amount

    def __ne__(self, other):
        return self.amount != other.amount

    def __gt__(self, other):
        return self.amount > other.amount

    def __ge__(self, other):
        return self.amount >= other.amount

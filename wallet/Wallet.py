import copy
import math

from logger.Logger import Logger
from model.money.Bitcoin import Bitcoin
from model.money.BitcoinCash import BitcoinCash
from model.money.Ethereum import Ethereum
from model.money.Euro import Euro
from model.money.Litcoin import Litcoin
from wallet.WalletStorage import WalletStorage


class Wallet:
    def __init__(self, initial_eur_balance=0):
        self.logger = Logger().get_logger()
        self.storage = WalletStorage()
        self._btc = Bitcoin(0)
        self._bch = BitcoinCash(0)
        self._eur = Euro(initial_eur_balance)
        self._eth = Ethereum(0)
        self._ltc = Litcoin(0)

        # Construction d'une map pour gérer les monnaies plus facilement
        self._moneys = {self._btc.currency: self._btc,
                        self._bch.currency: self._bch,
                        self._eur.currency: self._eur,
                        self._eth.currency: self._eth,
                        self._ltc.currency: self._ltc}

        # Récupère toutes les monnaies de la BDD
        self._retrieve_money_from_storage()
        # Les enregistre pour sauvegarder les nouvelles qui ne sont pas encore présentes en BDD
        self.storage.store_wallet(self)

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
                return money_in_wallet.amount >= money.amount or math.isclose(money_in_wallet.amount, money.amount)

    def get_money_list_in_wallet(self):
        # TODO : utiliser la map "moneys" définie dans la classe
        return [self._eur, self._btc, self._eth, self._ltc, self._bch]

    def print_balance(self):
        self.logger.info("==============")
        for moneyInWallet in self.get_money_list_in_wallet():
            self.logger.info(moneyInWallet)
        self.logger.info("==============")

    def has_moneys(self):
        for money in self.get_money_list_in_wallet():
            if money.amount > 0.1:
                return True
        return False

    def __operation_on_wallet(self, money):
        for money_in_wallet in self.get_money_list_in_wallet():
            if money.currency == money_in_wallet.currency:
                money_in_wallet.amount += money.amount
                self.storage.store_money(money_in_wallet)

    def _retrieve_money_from_storage(self):
        for id, money in self._moneys.items():
            stored_money = self.storage.get_money(money.currency)
            if stored_money is not None:
                #TODO: Comment faire ça proprement en python.... !?!
                if stored_money.currency == "EUR":
                    self._eur = stored_money
                if stored_money.currency == "BCH":
                    self._bch = stored_money
                if stored_money.currency == "BTC":
                    self._btc = stored_money
                if stored_money.currency == "ETH":
                    self._eth = stored_money
                if stored_money.currency == "LTC":
                    self._ltc = stored_money

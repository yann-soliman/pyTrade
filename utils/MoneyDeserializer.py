
from model.money.Bitcoin import Bitcoin
from model.money.BitcoinCash import BitcoinCash
from model.money.Ethereum import Ethereum
from model.money.Euro import Euro
from model.money.Litcoin import Litcoin
from model.money.Dollar import Dollar


class MoneyDeserializer:
    @staticmethod
    def deserialize(currency, amount=0):
        """
        "Désérialize" une currency sous forme de string en Money
        :param currency:
        :return:
        """
        if currency == "BCH":
            return BitcoinCash(amount)
        if currency == "EUR":
            return Euro(amount)
        if currency == "BTC":
            return Bitcoin(amount)
        if currency == "ETH":
            return Ethereum(amount)
        if currency == "LTC":
            return Litcoin(amount)
        if currency == "USD":
            return Dollar(amount)

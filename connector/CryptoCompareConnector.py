import requests
from expiringdict import ExpiringDict

from model.money.Money import Money
from utils.MoneyDeserializer import MoneyDeserializer


class CryptoCompareConnector():
    URL = "https://min-api.cryptocompare.com"

    def __init__(self):
        self.cache = ExpiringDict(max_len=100, max_age_seconds=10)

    def get_price_in_euro(self, currency):
        if self.cache.get(currency) is None:

            # Appel HTTP
            params = {"fsym":currency, "tsyms" : self._get_tsyms(currency)}
            try:
                r = requests.get(self.URL + '/data/price', params=params)
                json_price = r.json()
                # TODO: pour l'instant on retourne juste le premier item mais on pourrait parcourir tous les items et les convertir
                first_currency = next(iter(json_price))
                first_price = next(iter(json_price.values()))
                money = MoneyDeserializer.deserialize(first_currency, first_price)
                self.cache[currency] = self._convert_currency_to_eur(money).amount
            except Exception:
                return None
        return self.cache[currency]

    def _convert_currency_to_eur(self, money):
        # TODO : rendre cette fonction plus générique et pouvoir convertir en n'importe quelle devise
        """
        Converti une money "montant/devise" en €
        :param money:
        :param currency:
        :return:
        """
        if Money.is_crypto_money(money):
            # Conversion d'une valeur crypto en valeur non crypto (USD, EUR, ...)
            price = self.get_price_in_euro(money.currency)
            return MoneyDeserializer.deserialize("EUR", price * money.amount)
        elif money.currency == "EUR":
            return money
        elif money.currency == "USD":
            # TODO : appeler une api de conversion de devise non crypto
            price = money.amount * 0.848068524
            return MoneyDeserializer.deserialize("EUR", price)

    def _get_tsyms(self, currency):
        """
        Retourne une string avec les devises (séparé par des virgules) vers lesquelles effectuer l'opération
        :param currency:
        :return:
        """
        if currency == "BCH":
            return "BTC"
        # Par défaut on demande de l'USD qui est la devise la plus répandu
        else:
            return "USD"

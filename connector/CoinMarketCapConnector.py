import urllib.request

import requests
from bs4 import BeautifulSoup


class CoinMarketCapConnector():
    COIN_MARKET_CAP_URL = "https://coinmarketcap.com/currencies/{}"
    COIN_MARKET_CAP_API_URL = "https://api.coinmarketcap.com/v1"

    def __init__(self):
        # Page en cours de parsing
        self.page = None

    def get_average_markets_price(self, currency1, currency2, limit=10):

        # Conversion de la devise demandée vers nom de la devise dans l'URL
        request_currency = self._map_currency_to_request(currency1)
        url = self.COIN_MARKET_CAP_URL.format(request_currency)

        # Appel HTTP
        self.page = urllib.request.urlopen(url).read()

        # Parsing de la réponse pour extraire :
        soup = BeautifulSoup(self.page, "lxml")

        # Combinaison : {Nom du marché : prix en USD}
        price_by_market = {}
        markets = soup.find(id="markets-table").tbody.find_all('tr')
        for row in markets[0:limit]:
            cols = row.find_all('td')
            name = cols[1].text.strip()
            pair = cols[2].text.strip()
            # On dégage le premier char du prix qui est "$123.123"
            usd_price = float(cols[4].text.strip()[1:])
            currency_price = self._convert_usd_amount_into_currency(usd_price, currency2)
            price_by_market[name] = {"price": currency_price}

        # Réinitialise la page à none
        self.page = None
        return price_by_market

    def get_market_cap(self):
        r = requests.get(self.COIN_MARKET_CAP_API_URL + "/global/")
        if r.status_code is 200:
            return float(r.json()["total_market_cap_usd"])

    def _map_currency_to_request(self, currency):
        if currency == "BCH":
            return "bitcoin-cash"

    def _get_currency_usd_exchange_rates(self, currency):
        # Parsing de la page pour extraire les taux de conversions
        soup = BeautifulSoup(self.page, "lxml")
        currency_exchange_rates = soup.find(id="currency-exchange-rates")
        return float(currency_exchange_rates['data-' + currency.lower()])

    def _convert_usd_amount_into_currency(self, amount_in_usd, currency):
        currency_rate = self._get_currency_usd_exchange_rates(currency)
        return amount_in_usd / currency_rate

import time

from Market import Market
from OrderBook import OrderBook
from model.ExchangeRate import ExchangeRate
from model.money.Bitcoin import Bitcoin
from model.money.Ethereum import Ethereum
from model.money.Euro import Euro


class DifferentPathSimulator:
    """
    Classe regroupant une simulation d'achat un "chemin" différent (à défaut de meilleur nom...)
    Le but est par exemple de regarder le prix BTC-EUR et le prix BTC-ETH, ETH-EUR pour constater qu'il est plus avantageux d'acheter
    d'abord de l'ETH puis de le revendre contre des EUR

    Simulation effectuée sur GDAX qui a des fees pour makers à 0%
    """

    def simulate(self):
        market = Market()
        market.add_euro_on_wallet(100)
        order_book = OrderBook()

        while True:
            btc_eur_bids = order_book.get_best_bids_price('BTC-EUR')
            btc_eur_asks = order_book.get_best_asks_price('BTC-EUR')
            exchange_rate_btc_eur = ExchangeRate(Bitcoin(1), Euro(btc_eur_asks))

            eth_btc_bids = order_book.get_best_bids_price('ETH-BTC')
            eth_btc_asks = order_book.get_best_asks_price('ETH-BTC')
            exchange_rate_eth_eur = ExchangeRate(Ethereum(1), Bitcoin(eth_btc_asks))

            eth_eur_bids = order_book.get_best_bids_price('ETH-EUR')
            eth_eur_asks = order_book.get_best_asks_price('ETH-EUR')
            exchange_rate_eth_eur = ExchangeRate(Ethereum(1), Euro(eth_eur_asks))

            print(exchange_rate_btc_eur, "BTC-EUR calculated : ", eth_eur_bids / eth_btc_asks)
            print(exchange_rate_eth_eur, "ETH-BTC calculated : ", eth_eur_bids / btc_eur_asks)
            print(exchange_rate_eth_eur, "ETH-EUR calculated : ", btc_eur_bids * eth_btc_asks)

            # if btc_eur_asks < eth_eur_bids/eth_btc_asks:
            #     current_euro = market.get_balance("EUR")
            #     eth_amount_to_buy = current_euro / eth_eur_bids
            #     market.buy(eth_amount_to_buy, "ETH", current_euro, "EUR")
            #
            #     market.print_balance()
            #     current_eth = market.get_balance("ETH")
            #     btc_amount_to_buy = eth_btc_asks * current_eth
            #     market.buy(btc_amount_to_buy, "BTC", current_eth, "ETH")

            amount_euro_before = market.get_balance("EUR")
            if eth_eur_asks >= btc_eur_bids * eth_btc_asks:
                # On achète X euro de bitcoin
                current_money_euro = market.get_balance("EUR")
                btc_amount_to_buy = current_money_euro.amount / btc_eur_asks
                btc_to_buy = Bitcoin(btc_amount_to_buy)
                market.buy(btc_to_buy, Euro(btc_eur_asks))

                # Grâce à nos bitcoins tout fraichement acquis, on achète de l'ETH
                current_btc = market.get_balance("BTC")
                eth_amount_to_buy = current_btc.amount / eth_btc_asks
                eth_to_buy = Ethereum(eth_amount_to_buy)
                market.buy(eth_to_buy, Bitcoin(eth_btc_asks))

                # Qu'on revend pour de bons vieux euros
                current_eth = market.get_balance("ETH")
                market.sell(current_eth, Euro(eth_eur_asks))

                # On compare le gain par rapport à si on l'avait acheté directement au prix du marché
                gain = market.get_balance("EUR").amount - amount_euro_before.amount
                print(gain)
                market.print_balance()
                time.sleep(1)
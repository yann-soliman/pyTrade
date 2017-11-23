class ExchangeRateCalculator:

    @staticmethod
    def convert(origin_money, exchange_rate_money):
        """
        Converti origin_money en exchange_rate_money
        :param origin_money: la Money à convertir (exemple : 0.5 BTC)
        :param exchange_rate_money: Le taux de conversion (exemple : 1500 €)
        :return:
        """
        amount = origin_money.amount * exchange_rate_money.amount
        return exchange_rate_money.get_same_currency_money_with_amount(amount)
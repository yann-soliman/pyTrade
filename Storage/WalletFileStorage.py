from tinydb import TinyDB, Query

from simulator.MoneyDeserializer import MoneyDeserializer


class WalletFileStorage:
    def __init__(self):
        self.storage = TinyDB('db.json')

    def store_wallet(self, wallet):
        for money in wallet.get_money_list_in_wallet():
            self.store_money(money)

    def store_money(self, money):
        query = Query()
        self.storage.upsert({"currency": money.currency, "amount": money.amount}, query.currency == money.currency)

    def get_money(self, currency):
        query = Query()
        serialized_money = self.storage.get(query.currency == currency)
        if serialized_money is None:
            return None
        return MoneyDeserializer.deserialize(serialized_money["currency"], serialized_money["amount"])

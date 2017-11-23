from storage.Storage import Storage
from utils.MoneyDeserializer import MoneyDeserializer


class WalletStorage:
    def __init__(self):
        self.storage = Storage().get_storage()

    def store_wallet(self, wallet):
        for money in wallet.get_money_list_in_wallet():
            self.store_money(money)

    def store_money(self, money):
        self.storage.upsert(money.currency, {"currency": money.currency, "amount": money.amount})

    def get_money(self, currency):
        serialized_money = self.storage.get(currency)
        if serialized_money is None:
            return None
        return MoneyDeserializer.deserialize(serialized_money["currency"], serialized_money["amount"])

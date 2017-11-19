from Storage.RedisStorage import RedisStorage


class WalletRedisStorage:

    def __init__(self):
        self.storage = RedisStorage()

    def store_wallet(self, wallet):
        for money in wallet.get_money_list_in_wallet():
            self.store_money(money)

    def store_money(self, money):
        self.storage.set(money.currency, money.amount)

    def get_money(self, currency):
        return self.storage.get(currency)

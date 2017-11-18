from model.money.Money import Money


class Ethereum(Money):

    def __init__(self, amount=0):
        super().__init__(amount)
        self.currency = "ETH"
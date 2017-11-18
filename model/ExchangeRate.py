class ExchangeRate:
    """
    Représente un taux de change de money1 <-> money2
    Exemple : 1 BCH <-> 1619 €
    """
    def __init__(self, money1, money2):
        self.money1 = money1
        self.money2 = money2

    def __str__(self):
        return "[" + str(self.money1.amount) + " " + self.money1.currency + " <-> " + str(self.money2.amount) + " " + self.money2.currency
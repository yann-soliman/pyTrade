import logging
import os

from config.Config import Config
from simulator.GdaxCompulsifSimulator import GdaxCompulsifSimulator

logging.basicConfig(format="%(levelname) -10s %(asctime)s | %(module)s:%(lineno)s | %(funcName)s | %(message)s",
                    level=logging.INFO)

#TODO : voir pour utiliser ça : https://github.com/nlsdfnbch/bitex
def main():
    # simulator = ComparatorSimulator()
    currency = os.environ.get('CURRENCY', "ETH")
    simulator = GdaxCompulsifSimulator(currency)
    simulator.simulate()



if __name__ == "__main__":
    config = Config()
    main()

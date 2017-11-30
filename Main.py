import logging

from alert.EmailAlert import EmailAlert
from config.Config import Config

logging.basicConfig(format="%(levelname) -10s %(asctime)s | %(module)s:%(lineno)s | %(funcName)s | %(message)s",
                    level=logging.INFO)

#TODO : voir pour utiliser ça : https://github.com/nlsdfnbch/bitex
def main():
    # simulator = ComparatorSimulator()
    # currency = os.environ.get('CURRENCY', "ETH")
    # simulator = GdaxCompulsifSimulator(currency)
    # simulator.simulate()

    emailAlert = EmailAlert()
    emailAlert.send_simple_message()


if __name__ == "__main__":
    config = Config()
    main()

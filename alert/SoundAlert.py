from logger.Logger import Logger


class SoundAlert:

    def __init__(self):
        self.logger = Logger().get_logger()
    # TODO : sound sur windows avec winsound, sur linux... ?

    def alert_buy(self):
        # winsound.PlaySound('sounds/sound.wav', winsound.SND_FILENAME)
        self.logger.info("ALERTE : BUY !")

    def alert_sell(self):
        # winsound.PlaySound('sounds/no.wav', winsound.SND_FILENAME)
        self.logger.info("ALERTE : SELL !")

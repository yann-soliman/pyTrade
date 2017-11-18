import logging
import gdax

logger = logging.getLogger(__name__)


class OrderBook:

    def __init__(self):
        self.public_client = gdax.PublicClient()

    def get_best_bids_price(self, product_id):
        return float(self.public_client.get_product_order_book(product_id)['bids'][0][0])

    def get_best_asks_price(self, product_id):
        return float(self.public_client.get_product_order_book(product_id)['asks'][0][0])

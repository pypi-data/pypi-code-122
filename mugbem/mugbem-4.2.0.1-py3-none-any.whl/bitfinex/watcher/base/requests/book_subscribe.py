from .base import AbstractRequest


class BookSubscribe(AbstractRequest):
    def __init__(self, symbol, precision='R0'):
        super(BookSubscribe, self).__init__()
        self.symbol = symbol
        self.precision = precision

    def get_channel(self) -> str:
        return 'book'

    def get_params(self) -> dict:
        return {
            'symbol': self.symbol,
            'prec': self.precision
        }

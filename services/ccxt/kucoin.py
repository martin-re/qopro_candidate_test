import ccxt
from ccxt.base.errors import BadSymbol

from services._utils import *


class KucoinService:
    """TODO:"""

    def __init__(self, config: dict | None = None) -> ccxt.Exchange:
        if config:
            self._exchange = ccxt.kucoin(config=config)
        else:
            self._exchange = ccxt.kucoin()

    def get_currency_price_from_ticker(self, currency_argument: str) -> CurrenciesRow:
        if not (symbol := translate_to_usdt_paired_symbol(currency_argument)):
            raise BadSymbol()
        ticker = self._exchange.fetch_ticker(symbol)

        return CurrenciesRow(
            currency=currency_argument,
            date_=round_milliseconds_to_seconds(ticker['timestamp']),
            price=ticker['bid'],
        )

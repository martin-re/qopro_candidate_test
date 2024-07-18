from collections import namedtuple

CurrenciesRow = namedtuple('CurrenciesRow', ['currency', 'date_', 'price'])


def translate_to_usdt_paired_symbol(currency_argument: str) -> str | bool:
    try:
        return '-'.join(currency_argument.upper().split('USDT')) + 'USDT'
    except:
        return False


def round_milliseconds_to_seconds(milliseconds: int) -> int:
    return round(milliseconds / 1000)

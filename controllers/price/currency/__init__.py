import http

from aiohttp.web_request import Request
from aiohttp.web import Response

from controllers._abc import Controller
from services.db.currencies import CurrenciesService
from services.ccxt.kucoin import KucoinService


class Get(Controller):
    @property
    def _parametrised(self) -> bool:
        return True
    
    async def handler(self, request: Request) -> Response:
        try:
            currency = request.match_info.get('currency')
            row = KucoinService().get_currency_price_from_ticker(currency)
            currencies_service = CurrenciesService()
            result = currencies_service.insert(row)
            return Response(status=http.HTTPStatus.OK, text=str(result.last_inserted_params))
        except Exception as ex:
            print(ex)
            return Response(status=http.HTTPStatus.NOT_FOUND)

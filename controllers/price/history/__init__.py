import http

from aiohttp.web_request import Request
from aiohttp.web import Response

from ..._abc import Controller


class Get(Controller):

    @property
    def _parametrised(self) -> bool:
        return False
    
    # FIXME: implement logic
    async def handler(self, request: Request) -> Response:
        return Response(status=http.HTTPStatus.SERVICE_UNAVAILABLE)


class Delete(Controller):
    
    @property
    def _parametrised(self) -> bool:
        return False
    
    # FIXME: implement logic
    async def handler(self, request: Request) -> Response:
        return Response(status=http.HTTPStatus.SERVICE_UNAVAILABLE)

# 1. GET /price/{currency}
# - Get last “bid” price from “kucoin” exchange of the coin (currency argument) paired to USDT (ioiusdt for example) 
#   and save it into database with actual timestamp rounded to seconds. In case currency not found, return HTTP 400 error code.
# 2. GET /price/history?page={page}
# - Get records from database (paginated) where page size is 10
# 3. DELETE /price/history
# - Delete all records in database
from aiohttp import web

from .price.currency import Get as GetPriceCurrency
from .price.history import Get as GetPriceHistory
from .price.history import Delete as DeleteHistory

__all__ = [
    'GetPriceCurrency', 
    'GetPriceHistory', 
    'DeleteHistory', 
    'app_factory'
]


# TODO: log registered controllers
class app_factory:
    """Web app factory, supports Gunicorn middleware."""

    def __new__(cls, middleware = None) -> web.Application:
        app = web.Application()
        # get controller names from __all__
        all_cp = [*__all__]
        all_cp.remove(cls.__name__)
        # get refs by names from namespace
        controllers = list(map(lambda ctl: globals().get(ctl)(), all_cp))
        # sort controllers, unparametrised ... parametrised
        controllers.sort(key=lambda ctl: ctl._parametrised)
        # register handlers
        try:
            for ctl in controllers:
                route_rule = ctl.method, ctl.path, ctl.handler
                app.router.add_route(*route_rule)
                # app.logger.info(f'Added rule: {route_rule}')
                print(f'Added rule: {route_rule}')
        except:
            ...

        return app

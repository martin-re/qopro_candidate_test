# Create REST API that will be deploy-able through “gunicorn” server as well as runnable as python module
import aiohttp.web as web

from models import *
from controllers import *

if __name__ == '__main__':
    app = app_factory()
    web.run_app(app)
else:
    # TODO: CREATE GUNICORN MIDDLEWARE
    middleware = object
    app = app_factory(middleware=middleware)

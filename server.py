# Create REST API that will be deploy-able through “gunicorn” server as well as runnable as python module

# 1. GET /price/{currency}
# - Get last “bid” price from “kucoin” exchange of the coin (currency argument) paired to USDT (ioiusdt for example) 
#   and save it into database with actual timestamp rounded to seconds. In case currency not found, return HTTP 400 error code.
# 2. GET /price/history?page={page}
# - Get records from database (paginated) where page size is 10
# 3. DELETE /price/history
# - Delete all records in database

import json
import asyncio
from typing import Any

import aiohttp.web as web
from aiohttp.web_request import Request
from aiohttp.web import Response

import ccxt.async_support as ccxt # link against the asynchronous version of ccxt
from ccxt.base.errors import BadSymbol
import sqlalchemy

kucoin = ccxt.kucoin()

# HELPERS (TODO: design pattering)
def round_milliseconds_to_seconds(milliseconds):
    return round(milliseconds / 1000)


def translate_to_exchange_pair_symbol(currency_argument: str) -> str | bool:
    try:
        return '-'.join(currency_argument.upper().split('USDT')) + 'USDT'
    except:
        return False


def insert_into_currencies(
        currency: str,
        date_: int,
        price: float,
    ) -> sqlalchemy.CursorResult[Any]:
    ins = currencies.insert().values(
        currency=currency,
        date_=date_,
        price=price,
    )
    with engine.connect() as conn:
        result = conn.execute(ins)
        conn.commit()

    return result


def select_from_currencies(pagination: int) -> sqlalchemy.CursorResult[Any]:
    sel = currencies.select().limit(pagination)
    with engine.connect() as conn:
        result = conn.execute(sel)
        conn.commit()

    return result


def delete_currencies():
    # query doesn't returns rows
    del_ = currencies.delete()
    with engine.connect() as conn:
        result = conn.execute(del_)
        conn.commit()



# CONTROLLERS
async def get_currency_price(request: Request) -> Response:
    try:
        currency_argument = request.match_info.get('currency') # (ioiusdt for example)
        if not (symbol := translate_to_exchange_pair_symbol(currency_argument)):
            raise BadSymbol()
        ticker = await kucoin.fetch_ticker(symbol)
    except BadSymbol as ex:
        print(ex)
        return Response(status=400)
    
    result = insert_into_currencies(
        currency=currency_argument,
        date_=round_milliseconds_to_seconds(ticker['timestamp']),
        price=ticker['bid'],
    )

    response_content = json.dumps(result.last_inserted_params())

    return Response(status=200, text=response_content)


async def get_history_paginated(request: Request) -> Response:
    try:
        pagination = request.rel_url.query.get('page')
        result = select_from_currencies(pagination)
        response_content = json.dumps([_._asdict() for _ in result.fetchall()])
        return Response(status=200, text=response_content)
    except:
        return Response(status=500)


async def delete_history(request: Request) -> Response:
    try:
        delete_currencies()
    except:
        return Response(status=500)
    return Response(status=200)


# SQALCHEMY
meta = sqlalchemy.MetaData()

currencies = sqlalchemy.Table(
'currencies', meta,
sqlalchemy.Column('id', sqlalchemy.Integer, primary_key = True), 
sqlalchemy.Column('currency', sqlalchemy.String),
sqlalchemy.Column('date_', sqlalchemy.BigInteger),
sqlalchemy.Column('price',sqlalchemy.Float)
)

db_username='postgres'
db_password='1234'
db_host='127.0.0.1'
db_port='5432'
db_name='postgres'

engine = sqlalchemy.create_engine(f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}')
meta.create_all(engine)

try:
    with engine.connect() as connection:
        print("Connection to the database successful")
except Exception as e:
    print(f"Error connecting to the database: {e}")

# AIOHTTP
web_app = web.Application()
web_app.router.add_routes([
    web.get('/price/history', get_history_paginated),
    web.delete('/price/history', delete_history),
    # parametrized URI
    web.get('/price/{currency}', get_currency_price),
])

# STAND-ALLONE RUN
if __name__ == '__main__':
    web.run_app(web_app)
else:
    # GUNICORN MIDDLEWARE
    ...

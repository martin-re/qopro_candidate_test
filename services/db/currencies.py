from typing import Any
import sqlalchemy

from models import *
from services._utils import *


# FIXME: Service should be for many tables, not for one
class CurrenciesService:
    """TODO: config"""

    __db_username='postgres'
    __db_password='1234'
    __db_host='127.0.0.1'
    __db_port='5432'
    __db_name='postgres'
    engine = sqlalchemy.create_engine(
        f'postgresql://{__db_username}:{__db_password}@{__db_host}:{__db_port}/{__db_name}'
    )
    meta.create_all(engine)

    try:
        with engine.connect():
            print("Connection to the database successful")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

    def __init__(self) -> None:
        self._query = ''

    def __str__(self) -> str:
        return self._query

    @property
    def _table(self) -> sqlalchemy.Table[currencies]:
        return currencies

    # TODO: complete
    def insert(self, row: CurrenciesRow) -> sqlalchemy.CursorResult[Any]:
        # self._query = self._table.insert().values(**row._asdict())
        self._query = self._table.insert().values(
            currency=row.currency,
            date_=row.date_,
            price=row.price
        )
        with self.engine.connect() as conn:
            result = conn.execute(self._query)
            conn.commit()

        return result

    def select(self):
        ...

    def delete(self):
        ...

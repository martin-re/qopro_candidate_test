# One table named currencies with PK named “id”,currency as “currency”,timestampas “date_”, price as “price”
from sqlalchemy import Table, Column, Integer, String, MetaData, Float, BigInteger

meta = MetaData()

currencies = Table(
   'curencies', meta,
   Column('id', Integer, primary_key = True), 
   Column('currency', String),
   Column('date_', BigInteger),
   Column('price',Float)
)

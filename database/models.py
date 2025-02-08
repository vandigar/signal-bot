from .db import BasicModel
from sqlalchemy import Column, String, Numeric, Date, ForeignKey, Integer

class DBModelStock (BasicModel):
    __tablename__ = "stocks"

    symbol = Column(String(10), unique=True)
    name = Column(String(40))
    exchange = Column(String(10))
    asset_type = Column(String(10))
    ipo_date = Column(Date)
    status = Column(String(10))


class DBModelStockLevel (BasicModel):
    __tablename__ = "stock_levels"

    symbol = Column(String(10), ForeignKey("stocks.id"))
    weight = Column(Integer)
    level = Column(Numeric(10,2))


class DBModelCriptoLevel(BasicModel):
    __tablename__ = "cripto_levels"

    symbol = Column(String(10))
    level = Column(Numeric(20, 10))





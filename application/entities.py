from pydantic import BaseModel
from typing import Optional, Annotated, Dict
from datetime import date, datetime
from abc import ABC, abstractmethod


class AbstractPydantic(BaseModel, ABC):
    pass

class Candle(AbstractPydantic):
    date: date
    high: float
    low: float
    open: float
    close: float
    volume: int

    class Config:
        extra = "ignore"


class MACD(AbstractPydantic):
    date: date
    macd_hist: float
    macd_signal: float
    macd: float

    class Config:
        extra = "ignore"


class Stock(AbstractPydantic):
    symbol: str
    name: str
    exchange: str
    asset_type: str
    ipo_date: Optional[date]
    status: str

    class Config:
        extra = "ignore"


class StockLevel(BaseModel):
    symbol: str
    weight: int
    level: float

class CriptoLevel(BaseModel):
    symbol: str
    level: float

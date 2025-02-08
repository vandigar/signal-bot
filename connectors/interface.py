from abc import ABC, abstractmethod
from application.entities import Candle, MACD, Stock


class ExternalDataSourceConnector(ABC):

    #naming rule: what you want to execute is the first, timeframe is optional and is the second.

    @abstractmethod
    def get_macd_weekly(self) -> list[MACD]:
        pass

    @abstractmethod
    def get_candles_weekly(self) -> list[Candle]:
        pass

    @abstractmethod
    def get_list_actual(self) -> list[Stock]:
        pass
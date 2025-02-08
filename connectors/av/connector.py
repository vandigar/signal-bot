import requests
from enum import Enum
from connectors.interface import ExternalDataSourceConnector as ExtDSC
from io import StringIO
import logging
from serializer import AVSerializer as AVS


API_2KEY = "7HXTVX58JHL7ZMGL"
# api_source: https://www.alphavantage.co/documentation/


class Timeframe(Enum):
    MIN_1 = "1min"
    MIN_5 = "5min"
    MIN_15 = "15min"
    MIN_30 = "30min"
    HOURLY = "60min"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class AVConnectorAPIV1:
    def __init__(self, apikey:str = API_2KEY):
        self.apikey = apikey
        self.base_url = "https://www.alphavantage.co/query?"

    def __get_data(self, **kwargs):
        url = f'{self.base_url}' + '&'.join([f"{key}={value}" for key, value in kwargs.items()]) + f'&apikey={self.apikey}'
        r = requests.get(url)
        return  r

    def _get_json_data(self, **kwargs):
        r = self.__get_data(**kwargs)

        data = r.json()
        return data

    def _get_csv_data(self, **kwargs):
        r = self.__get_data(**kwargs)

        if r.status_code == 200:
            csvfile = StringIO(r.text)
            return csvfile
        else:
            logging.error(f"Ошибка при запросе CSV данных: HTTP {r.status_code}")


class AVDataExecutor(AVConnectorAPIV1, ExtDSC):
    def get_macd_weekly(self):
        data = self._get_json_data(
            function = 'MACDEXT',
            interval = Timeframe.WEEKLY.value,
            series_type = 'open',
            apikey = self.apikey
        )
        objects = AVS.json_to_macd_objects(data)
        return objects

    def get_candles_weekly(self):
        # url example: https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=IBM&apikey=demo
        data = self._get_json_data(
            function = 'TIME_SERIES_WEEKLY_ADJUSTED&',
            adjusted = True
        )
        objects = AVS.json_to_candle_objects(data)
        return objects

    def get_list_actual(self):
        data = self._get_json_data(
            function='LISTING_STATUS',
            apikey = self.apikey
        )
        objects = AVS.csv_to_stocks_objects(data)
        return objects

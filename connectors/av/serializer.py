from application.entities import Candle, MACD, Stock
from datetime import datetime
import csv


class AVSerializer:
    @staticmethod
    def json_to_candle_objects(market_data):
        objects_list = []
        time_series_data = market_data['Weekly Adjusted Time Series']
        for date, values in time_series_data.items():
            obj = Candle(
                date=datetime.strptime(date, "%Y-%m-%d"),
                open=values["1. open"],
                high=values["2. high"],
                low=values["3. low"],
                close=values["5. adjusted close"],
                volume=values["6. volume"]
            )
            objects_list.append(obj)
        return objects_list

    @staticmethod
    def json_to_macd_objects(market_data):
        objects_list = []
        time_series_data = market_data['Technical Analysis: MACDEXT']
        for date, values in time_series_data.items():
            obj = MACD(
                date=datetime.strptime(date, "%Y-%m-%d"),
                macd=values["MACD"],
                macd_hist=values["MACD_Hist"],
                macd_signal=values["MACD_Signal"]
            )
            objects_list.append(obj)
        return objects_list

    @staticmethod
    def csv_to_stocks_objects(csv_list: csv):
        objects_list = []
        reader = csv.DictReader(csv_list)
        for row in reader:
            print(row)
            obj = Stock(
                symbol=row["symbol"],
                name=row["name"],
                exchange=row["exchange"],
                asset_type=row["assetType"],
                ipo_date=datetime.strptime(row["ipoDate"],"%Y-%m-%d"),
                status=row["status"]
            )
            objects_list.append(obj)
        return objects_list
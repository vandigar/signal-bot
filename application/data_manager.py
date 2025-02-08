from connectors.av.interface import get_actual_stock_list, get_weekly_candles, get_weekly_macd_candles
from processor.resistance_levels.processor import find_levels
from processor.resistance_levels.experimental import exp_find_levels
from .entities import StockLevel
from database.repo import StockRepo, LevelsRepo
from application.entities import Stock
from typing import List


async def update_stocks_list():
    actual_objects = get_actual_stock_list()
    repo = StockRepo()
    for object in actual_objects:
        if not await repo.check_stock(object.symbol):
            await repo.add_stock(object)

    # there is no validation for delisted units


async def update_weekly_tf_stocks_levels():
    #*yflj jxbofnm ehjdyb tot gthtl гзвфеу;
    stock_repo = StockRepo()
    levels_repo = LevelsRepo()

    stock_list: List[Stock] = await stock_repo.get_stock_list() # тут надо получение скаляра сделать

    for stock in stock_list:
        print(f"Начали обработку {stock.symbol}")
        candles_list = get_weekly_candles(stock.symbol)
        print(f"Получили свечи  {stock.symbol}")
        macd_list = get_weekly_macd_candles(stock.symbol)
        print(f"Получили macd {stock.symbol}")
        complex_level_list = find_levels(macd_candles=macd_list, candles=candles_list)
        print(f"Нашли уровни {stock.symbol}")

        print(f" уровни такие: {complex_level_list}")

        for level in complex_level_list:
            stock_level = StockLevel(
                symbol=stock.symbol,
                weight=level['weight'],
                level= level['mid']
            )
            await levels_repo.add_stock_level(stock_level)

async def update_stock_level(symbol):
    levels_repo = LevelsRepo()

    print(f"Начали обработку {symbol}")
    candles_list = get_weekly_candles(symbol)
    print(f"Получили свечи  {symbol}")
    macd_list = get_weekly_macd_candles(symbol)
    print(f"Получили macd {symbol}")
    complex_level_list = find_levels(macd_candles=macd_list, candles=candles_list)
    print(f"Нашли уровни {symbol}")

    print(f" уровни такие: {complex_level_list}")

    await levels_repo.del_stock_levels(symbol=symbol)

    for level in complex_level_list:
        stock_level = StockLevel(
            symbol=symbol,
            weight=level['weight'],
            level=level['mid']
        )
        await levels_repo.add_stock_level(stock_level)

#Тестовая хуйня
async def preculc_stock_level(symbol):

    print(f"Начали обработку {symbol}")
    candles_list = get_weekly_candles(symbol)
    print(f"Получили свечи  {symbol}")
    macd_list = get_weekly_macd_candles(symbol)
    print(f"Получили macd {symbol}")
    exp_find_levels(macd_candles=macd_list, candles=candles_list)



async def get_existed_levels(symbol):
    pass


async def check_price():
    pass






"""



from .entities import Candle, CandleMACDExtension
from .connector import Connector, Timeframe
from .market_data_manager import JSONMarketData
from typing import List


def get_standard_candles(symbol: str):
    connector = Connector(symbol=symbol)
    connector.set_url_stock_weekly()
    market_data = JSONMarketData(market_data = connector.get_data())
    candles = market_data.to_candles()
    return candles


def get_macd(symbol: str):
    connector = Connector(symbol = symbol)
    connector.set_url_macd_ext(Timeframe.WEEKLY)
    market_data = JSONMarketData(market_data= connector.get_data())
    candles = market_data.to_macd_candles()
    return candles





def strategy():
    market_candles = get_standard_candles("CSCO")
    macd_candles = get_macd("CSCO")
    market_candles.reverse() #reverse т.к. исходник начинается с текущего момента и назад. Надо развернуть список.
    macd_candles.reverse()
    levels = get_levels(candles=market_candles, macd_candles=macd_candles)
    print(levels[-14:])
    print(len(levels))



"""



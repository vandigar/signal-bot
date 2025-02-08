"""
# Восходящий тренд

- min растет
- max растет

# Нисходящий тренд
- min падает
- max падает

# Горизонтальный канал
- min в заданном диапазоне не меняется
- max в заданном диапазоне не меняется

# Идентификация первого тренда

# Переход от роста / падения в горизонталь

# переход от горизонтали в рост падение

# Переход от падения в рост и наоборот

# Новый вид уровней: минимум тренда, максимум тренда.

"""

from application.entities import MACD, Candle
from typing import List
from .entities import SimpleLevel, LevelType
from pydantic import BaseModel
from datetime import date, datetime

class DatedSimpleLevel(BaseModel):
    price: float
    type: LevelType
    date: date
    comment: str = ""

def _find_channel(levels: List[SimpleLevel]):
    dated_levels = []
    for level in levels:
        d_level = DatedSimpleLevel(
            price=level.price,
            type=level.type,
            date=datetime.strptime(level.date, '%Y-%m-%d'),
            comment=level.comment
        )
        dated_levels.append(d_level)

    dated_levels.sort(key= lambda x: x.date)

    for level in dated_levels:
        print(f"first: {level}")

    # prepare data:
    trend = False
    iteration_trend = False
    trend_start = 0
    trend_end = 0
    finish_level = []
    i = 0
    while i < (len(dated_levels)-5):
    #надо заменить на while и двигаться по одному шагу, пока не найду тренд, а потом по два.
        if (
                dated_levels[i+0].price < dated_levels[i+2].price and
                dated_levels[i+1].price < dated_levels[i+3].price and
                dated_levels[i+2].price < dated_levels[i+4].price and
                dated_levels[i+3].price < dated_levels[i+5].price
        ): iteration_trend = True
        else: iteration_trend = False

       # print(f"i = {i}, iteration_trend = {iteration_trend}, trend = {trend}")
        if iteration_trend and not trend:
            trend = True
            trend_start = i
            trend_end = i + 4
            i += 2

        elif iteration_trend and trend:
            trend_end = i + 4
            i += 2

        elif not iteration_trend and trend:
            trend = False
            i += 1
            #запись данных
            finish_level.append(dated_levels[trend_start])
            finish_level.append(dated_levels[trend_end])

        elif not iteration_trend and not trend:
            i += 1
            pass




    for level in finish_level:
        print(level)



    # 11 - 21 - 33 - 51 - 118 - 170
    # upper_trend_searcher
    # if_upper_trend_started

    # search trend

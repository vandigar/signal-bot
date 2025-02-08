from application.entities import MACD, Candle
from typing import List
from .entities import ComplexLevel


def find_levels(macd_candles: List[MACD],
                candles: List[Candle]):
    #Расчет уровней
    simple_levels = _find_simple_levels(macd_candles=macd_candles, candles=candles)
    complex_levels = _set_complex_levels(raw_levels=simple_levels)
    filtered_levels = _filter_levels(complex_levels)

    list = []
    for level in filtered_levels:
        list.append(level.model_dump())
    return list

# ЭТО ОБЯЗАТЕЛЬНАЯ ХЕРЬ для работы
def _find_simple_levels(macd_candles: List[MACD], candles: List[Candle]):
    candles_scope = []
    dif_count = 0  # Счетчик свечей macd подряд которые не соответствует тренду.
    levels = [] # Массив из уровней поддержки
    trend = None
    i = 0
    macd_len = len(macd_candles)
    while i < macd_len:
        # ------------------ Определяем тренд
        if trend == None:
            if macd_candles[i].macd_hist >= 0:
                dif_count = 1 if dif_count < 0 else dif_count + 1
                i+=1

            elif macd_candles[i].macd_hist < 0:
                dif_count = -1 if dif_count > 0 else dif_count - 1
                i+=1

            if abs(dif_count) == 4:
                trend = True if dif_count > 0 else False
                i -=3
        # ------------------ Область бычьего тренда
        elif trend:
            if macd_candles[i].macd_hist >= 0:
                dif_count = 0
                candles_scope.append(macd_candles[i])
                i+=1
            elif macd_candles[i].macd_hist < 0 and dif_count < 4:
                dif_count += 1
                candles_scope.append(macd_candles[i])
                i+=1
            elif macd_candles[i].macd_hist < 0 and dif_count == 4:
                dif_count = 0
                candles_scope = candles_scope[:-3]
                level = _find_level(trend=trend, macd_candles_scope=candles_scope, candles=candles)
                levels.append(level)
                candles_scope.clear()
                trend = False
                i -= 3
        # ------------------ Область медвежьего тренда
        else:
            if macd_candles[i].macd_hist < 0:
                dif_count = 0
                candles_scope.append(macd_candles[i])
                i+=1
            elif macd_candles[i].macd_hist >= 0 and dif_count < 4:
                dif_count += 1
                candles_scope.append(macd_candles[i])
                i+=1
            elif macd_candles[i].macd_hist >= 0 and dif_count == 4:
                dif_count = 0
                candles_scope = candles_scope[:-3]
                level = _find_level(trend=trend, macd_candles_scope=candles_scope, candles=candles)
                levels.append(level)
                candles_scope.clear()
                trend = True
                i -= 3

    #возвращает просто набор числовых значений, которые являются уровнями с точки зрения стратегии поиска интервалов.
    return levels


def _find_level(trend: bool, macd_candles_scope: List[MACD], candles: List[Candle]):
    prices = []
    for i in range(len(macd_candles_scope)):
        date = macd_candles_scope[i].date
        candle = next((obj for obj in candles if obj.date == date), None)
        if candle:
            prices.append(candle.close)
    level = max(prices) if trend else min(prices)
    return level


def _set_complex_levels(raw_levels: List[float]):
    diverse = 0.045
    complex_levels = []
    for level in raw_levels:
        complex_level = ComplexLevel(
            mid=level,
            min=level * (1 - diverse),
            max=level * (1 + diverse)
        )
        complex_levels.append(complex_level)
    sorted_complex_levels = sorted(complex_levels, key=lambda x: x.mid)
    return sorted_complex_levels


def _filter_levels(complex_levels: List[ComplexLevel]):
    sorted_complex_levels = sorted(complex_levels, key=lambda x: x.mid)
    i = 0
    filtered_levels = []
    length = len(sorted_complex_levels)

    while i < length:
        weight = 0
        group_level = ComplexLevel(**sorted_complex_levels[i].model_dump())
        while i < length:
            weight += 1
            try:
                next_level = ComplexLevel(**sorted_complex_levels[i + 1].model_dump())
            except:
                group_level.weight = weight
                filtered_levels.append(group_level)
                i += 1
                break

            if group_level.mid < next_level.mid and group_level.max > next_level.mid:
                group_level.max = next_level.max
                group_level.mid = (next_level.mid + group_level.mid)/2
                i += 1
            elif group_level.mid > next_level.mid and group_level.min > next_level.min:
                group_level.min = next_level.min
                group_level.mid = (next_level.mid + group_level.mid)/2
                i += 1
            else:
                filtered_levels.append(group_level)
                group_level.weight = weight
                i += 1
                break

    return filtered_levels
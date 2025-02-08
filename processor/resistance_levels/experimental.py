from application.entities import MACDExt, Candle
from typing import List
from .entities import SimpleLevel, LevelType
from .channels import _find_channel

def exp_find_levels(macd_candles: List[MACDExt], candles: List[Candle]):
    # Расчет экстремумов волнового движения
    all_levels = _find_all_levels(macd_candles=macd_candles, candles=candles)
    if all_levels:
        _find_channel(levels=all_levels)
    """
    if all_levels:
        min_levels = _separate_min_max(simple_levels=all_levels, type = LevelType.MIN)
        max_levels = _separate_min_max(simple_levels=all_levels, type= LevelType.MAX)
        cross_levels_min =  _find_strong_cross_levels(src_levels=min_levels, control_levels=max_levels, delta=0.04)
        #cross_levels_max = _find_strong_cross_levels(src_levels=max_levels, control_levels=min_levels, delta=0.04)
        min_intype_levels = _find_strong_intype_levels(levels=min_levels, delta = 0.04)
        max_intype_levels = _find_strong_intype_levels(levels=max_levels, delta = 0.04)
        singleton_levels = _find_singleton_levels(levels=all_levels, delta=0.2)
        minmax = _find_minmax(all_levels)

        final_list = minmax + min_intype_levels + max_intype_levels + singleton_levels + cross_levels_min # + cross_levels_max

        final_list.sort(key= lambda x: x.price)

        dedoublicated = _filter_doubles(final_list)

        for level in dedoublicated:
            print(level)
    
    else: print(f"нет уровней чот")
    """

# Стретегия поиска:
## [+] Поиск ВСЕХ уровней по стратегии "macd + экстремум".
## [+] Разделение списков на минимальные и максимальные. итого три списка для работы: минимумы, максимумы, общий (на кой?)
# ----
## Множественные минимальные: поиск среди минимальных уровней уровней с минимальным отличием (сравнение двух списков )
## Можественные максимальные: поиск среди максимальных уровней уровней с минимальным отличием (сравнение двух списков)
## Одиночные максимальные: максимум у которого нет других минимумов/максимумов в "большом" диапазоне.
## Одиночные минимальные: минимум у которого нет других минимумов/максимумв в "большом диапазоне.
## Топовый максимум.
## ТОповый минимум.

# Стратегия устранения дублей:
## Чистые дубли
## Дубли в диапазоне

def _find_minmax(levels: List[SimpleLevel]):
    minmax = []
    levels.sort(key= lambda x: x.price)
    minmax.append(levels[0])
    minmax.append(levels[-1])
    return minmax

def _separate_min_max(simple_levels: List[SimpleLevel], type: LevelType):
    result_levels = []
    for level in simple_levels:
        if level.type == type: result_levels.append(level)

    result_levels.sort(key=lambda x: x.price)
    return result_levels

def _find_all_levels(macd_candles: List[MACDExt], candles: List[Candle]):
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
                level = __find_level(trend=trend, macd_candles_scope=candles_scope, candles=candles)
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
                level = __find_level(trend=trend, macd_candles_scope=candles_scope, candles=candles)
                levels.append(level)
                candles_scope.clear()
                trend = True
                i -= 3

    return levels

def __find_level(trend: bool, macd_candles_scope: List[MACDExt], candles: List[Candle]):
    crossed_candles = []
    prices = []
    # print (macd_candles_scope)

    for i in range(len(macd_candles_scope)):
        date = macd_candles_scope[i].date
        candle = next((obj for obj in candles if obj.date == date), None)
        if candle:
            crossed_candles.append(candle)


    extremum = max(crossed_candles, key = lambda  x: x.close) if trend else min(crossed_candles, key = lambda  x: x.close)

    level = SimpleLevel(
        price= extremum.close,
        type = LevelType.MAX if trend else LevelType.MIN,
        date = extremum.date
    )
    return level

def _find_strong_cross_levels (src_levels: List[SimpleLevel], control_levels: List[SimpleLevel],delta: float):
    #src_leevls - уровни которые мы проверяем на наличие пересечений с уровнями из второго списка.
    # control_level - уровни которые мы применяем к исходнику в поиске пересечений, подтверждения что уровень есть.
    p_delt = 1 + delta
    m_delt = 1 - delta

    #ищем точные схождения
    result_levels = []
    for src_level in src_levels:
        for control_level in control_levels:
            if src_level.price*p_delt > control_level.price and src_level.price*m_delt < control_level.price:
                src_level.comment = "strong_cross_level"
                result_levels.append(src_level)

    return result_levels

def _find_strong_intype_levels(levels: List[SimpleLevel], delta: float):
    p_delt = 1 + delta
    m_delt = 1 - delta

    # ищем точные схождения
    result_levels = []
    for i in range(len(levels)):
        for k in range(len(levels)):
            if k == i:
                break
            if levels[i].price*p_delt > levels[k].price and levels[i].price*m_delt < levels[k].price:
                levels[i].comment = f"strong_intype_level {levels[i].type}"
                result_levels.append(levels[i])
            k += 1
        i += 1
    return result_levels

def _find_singleton_levels(levels: List[SimpleLevel], delta: float):
    p_delt = 1 + delta
    m_delt = 1 - delta

    # ищем точные схождения
    result_levels = []
    for i in range(len(levels)):
        match = False
        for k in range(len(levels)):
            if (
                    levels[i].price * p_delt > levels[k].price and
                    levels[i].price * m_delt < levels[k].price and
                    i != k):
                match = True
                break
        if not match:
            levels[i].comment = "singleton level"
            result_levels.append(levels[i])


    return  result_levels

def _filter_doubles(levels: List[SimpleLevel]):
    res = []

    for level in levels:
        have_equal = False
        for res_level in res:
            if level.is_equal(res_level):
                have_equal = True
        if not have_equal: res.append(level)

    return res

def _advanced_filter_doubles(levels: List[SimpleLevel]):
    # Надо проанализировать изменение стоимости акции за все время. Насколько оно изменилось.
    ## Не изменлось / значительно выросло / Значительно упало
    pass


def _find_trends_by_levels(levels: List[SimpleLevel]):
    
    pass


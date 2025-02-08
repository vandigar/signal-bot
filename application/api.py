from fastapi import APIRouter
from application.data_manager import update_stocks_list, update_weekly_tf_stocks_levels, update_stock_level, preculc_stock_level


levels = APIRouter(prefix="/levels")


@levels.post("/update/",
          response_model=None,
          status_code=200)
async def update_stock_levels():
    await update_weekly_tf_stocks_levels()


list = APIRouter(prefix="/stock_list")


@list.post("/update/",
             response_model=None,
             status_code=200)
async def update():
    await update_stocks_list()

levels = APIRouter(prefix="/stock_levels")

@levels.post("/update_all/",
             response_model=None,
             status_code=200)
async def update_all():
    await update_weekly_tf_stocks_levels()

@levels.post("/update_current/",
             response_model=None,
             status_code=200)
async def update_current(symbol:str):
    await update_stock_level(symbol=symbol)

@levels.post("/preculc_current/",
             response_model=None,
             status_code=200)
async def preculc_current(symbol:str):
    await preculc_stock_level(symbol = symbol)
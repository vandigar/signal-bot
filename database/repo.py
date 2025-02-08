from .db import db_helper
from application.entities import Stock, StockLevel, CriptoLevel
from .models import DBModelStock, DBModelStockLevel, DBModelCriptoLevel
from sqlalchemy.future import select
from sqlalchemy import delete




class LevelsRepo:
    def __init__(
        self,
    ):
        self.session = db_helper.session_factory()

    # ---- STOCK ----
    # add_level
    async def add_stock_level(self, level: StockLevel):
        level_model = DBModelStockLevel(**level.model_dump())
        print(level_model.__dict__)
        self.session.add(level_model)
        await self.session.commit()
        return level_model


    # delete level
    async def del_stock_level(self, level_id: int):
        level_model = (
            await self.session.query(DBModelStockLevel).filter_by(id=level_id).first()
        )
        self.session.delete(level_model)
        await self.session.commit()

    async def del_stock_levels(self, symbol):
        await self.session.execute(delete(DBModelStockLevel).where(DBModelStockLevel.symbol == symbol))

    # get levels by symbol
    async def get_stock_levels(self, symbol: str):
        level_models = (
            await self.session.query(DBModelStockLevel).filter_by(symbol = symbol).all()
        )
        return level_models

    # get_level_by_id
    async def get_stock_level(self, level_id: id):
        level_models = (
            await self.session.query(DBModelStockLevel).filter_by(id = level_id).first()
        )
        return level_models

    # ---- CRIPTO ----
    # add_level
    async def add_cripto_level(self, level: CriptoLevel):
        level_model = DBModelCriptoLevel(**level.model_dump())
        self.session.add(level_model)
        await self.session.commit()
        return level_model


    # delete level
    async def del_cripto_level(self, level_id: int):
        level_model = (
            await self.session.query(DBModelCriptoLevel).filter_by(id=level_id).first()
        )
        self.session.delete(level_model)
        await self.session.commit()

    # get levels by symbol
    async def get_cripto_levels(self, symbol: str):
        level_models = (
            await self.session.query(DBModelCriptoLevel).filter_by(symbol = symbol).all()
        )
        return level_models

    # get_level_by_id
    async def get_cripto_level(self, level_id: id):
        level_models = (
            await self.session.query(DBModelCriptoLevel).filter_by(id = level_id).first()
        )
        return level_models

class StockRepo:
    def __init__(
            self,
    ):
        self.session = db_helper.session_factory()

    # get_symbols
    async def get_stock_list(self):
        query = select(DBModelStock)
        results = await self.session.execute(query)
        return results.scalars().all()

    async def check_stock(self, symbol):
        query = select(DBModelStock).filter_by(symbol=symbol)
        results = await self.session.execute(query)
        stock = results.first()
        return bool(stock)

    # add_symbol

    async def add_stock(self, stock: Stock):
        new_stock = DBModelStock(**stock.model_dump())
        self.session.add(new_stock)
        await self.session.commit()

    # delete_symbol
    async def del_stock(self, symbol: str):
        query = select(DBModelStock).filter_by(symbol=symbol)
        results = await self.session.execute(query)
        stock = results.first()
        self.session.delete(stock)
        await self.session.commit()

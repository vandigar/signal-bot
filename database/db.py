from sqlalchemy import create_engine, Column, DateTime, Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from datetime import datetime
from pydantic_settings import BaseSettings

Base = declarative_base()


# Tables templates
class BasicModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class TimeStampedModel(BasicModel):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())



# DB helper
class Setting(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./db.sqlite3"
    db_echo: bool = True

setting = Setting()

class DatabaseHelper:
    def __init__(self, url: str = setting.db_url, echo: bool = setting.db_echo):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )


db_helper = DatabaseHelper(setting.db_url, setting.db_echo)

from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from application.api import list as list_router
from application.api import levels as level_router
from database.migrations import check_for_migrations, upgrade_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    check_for_migrations()
    upgrade_database()
    yield


app = FastAPI(title="Trade Notificator", lifespan=lifespan)
app.include_router(list_router)
app.include_router(level_router)

async def start_app():
    config = uvicorn.Config(
        "application.app:app", host="127.0.0.1", port=8000, reload=True
    )
    server = uvicorn.Server(config)
    await server.serve()

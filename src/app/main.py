from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.api.router import router
from src.app.database.connection import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("INFO: Creating database tables...")
    await create_db_and_tables()
    yield

app = FastAPI(
    lifespan=lifespan,
    title="Knowledge Extractor System",
)


app.include_router(router, prefix=f"/api")



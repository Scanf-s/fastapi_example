# src/main.py
from fastapi import FastAPI
from sqlmodel import SQLModel

from config.settings import config
from config.database import Database
from jwt_token.routers import router as token_router


def create_app() -> FastAPI:
    # Database Initialize
    Database.init_engine(db_url=config.DATABASE_URL)

    # Create all tables
    SQLModel.metadata.create_all(Database.get_engine())

    # FastAPI Application Initialize
    fastapi: FastAPI = FastAPI(
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    # Register API Routers
    fastapi.include_router(token_router, prefix=config.BASE_API_URI, tags=["token"])

    # Just for test purpose...
    @fastapi.get("/")
    async def root():
        return {"message": "OK"}

    return fastapi

app = create_app()

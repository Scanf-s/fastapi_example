from fastapi import FastAPI
from config.exceptions import register_exception_handlers
from sqlmodel import SQLModel

from config.settings import config
from config.database import Database
from jwt_token.routers import router as token_router
from user.routers.user import router as user_router


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

    # Register Exception Handlers
    register_exception_handlers(fastapi)

    # Register API Routers
    fastapi.include_router(token_router, prefix=config.BASE_API_URI, tags=["token"])
    fastapi.include_router(user_router, prefix=config.BASE_API_URI, tags=["user"])

    # Just for test purpose...
    @fastapi.get("/")
    async def root():
        return {"message": "OK"}

    return fastapi

app = create_app()

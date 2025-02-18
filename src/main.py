from fastapi import FastAPI
from src.config import Config
from src.database import Database
from src.token.routers import router as token_router


fastapi_settings: Config = Config()
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.include_router(token_router, prefix=fastapi_settings.BASE_API_URI, tags=["token"])
Database.init_engine(db_url=fastapi_settings.DATABASE_URL)

@app.get("/")
async def root():
    return {"message": "OK"}

from fastapi import FastAPI
from src.config import Config
from src.database import Database

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
fastapi_settings: Config = Config()
Database.init_engine(db_url=fastapi_settings.DATABASE_URL)

@app.get("/")
async def root():
    return {"message": "Hello World"}

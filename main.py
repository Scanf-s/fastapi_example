from fastapi import FastAPI
from settings import fastapi_settings
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

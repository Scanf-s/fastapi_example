from typing import Generator
from sqlmodel import Session

from .database import Database
from .settings import config, Config

def get_fastapi_config() -> Config:
    """
    fastapi config 를 반환하는 FastAPI 의존성
    Depends로 의존성 주입 시 사용한다.
    """
    return config

def get_database_session() -> Generator:
    """
    데이터베이스 세션을 반환하는 FastAPI 의존성
    Depends로 의존성 주입 시 사용한다.
    """
    with Session(Database.get_engine()) as session:
        yield session

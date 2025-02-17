from sqlmodel import create_engine
from sqlalchemy.engine.base import Engine
from sqlmodel import SQLModel

from src.user.models import User

class Database:
    _engine: Engine = None

    @staticmethod
    def init_engine(db_url: str) -> None:
        Database._engine = create_engine(db_url, echo=True)
        SQLModel.metadata.create_all(Database.get_engine())

    @staticmethod
    def get_engine() -> Engine:
        if Database._engine is None:
            raise ValueError("Engine is not initialized. Call Database.init_engine() first.")
        return Database._engine

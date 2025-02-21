from typing import Optional

from sqlmodel import create_engine
from sqlalchemy.engine.base import Engine


class Database:
    _engine: Optional[Engine] = None

    @staticmethod
    def init_engine(db_url: str) -> None:
        Database._engine = create_engine(db_url, echo=True)

    @staticmethod
    def get_engine() -> Engine:
        if Database._engine is None:
            raise ValueError("Engine is not initialized. Call Database.init_engine() first.")
        return Database._engine

from sqlmodel import Field, SQLModel
import uuid
from enum import Enum

class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class Token(SQLModel, table=True):
    id: uuid.UUID = Field(default=None, primary_key=True)
    token: str = Field(index=True)
    type: TokenType = Field(default=TokenType.ACCESS)

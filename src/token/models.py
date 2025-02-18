from typing import Optional
import uuid
from sqlmodel import Field, SQLModel
from enum import Enum

class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class Token(SQLModel, table=True):
    token_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.user_id", index=True, unique=True)
    token: str = Field(index=True)
    type: TokenType = Field(default=TokenType.REFRESH)

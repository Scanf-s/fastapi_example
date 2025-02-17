from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: str
    is_active: bool
    role: UserRole = Field(default=UserRole.USER)
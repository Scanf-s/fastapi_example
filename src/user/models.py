from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel
import uuid

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(SQLModel, table=True):
    user_id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    email: str
    password: str
    is_active: bool
    role: UserRole = Field(default=UserRole.USER)
    
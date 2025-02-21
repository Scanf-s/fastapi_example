from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel
from sqlalchemy.schema import PrimaryKeyConstraint
import uuid

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class ThirdPartyProvider(str, Enum):
    GOOGLE = "google"
    NAVER = "naver"
    KAKAO = "kakao"
    TWITTER = "twitter"
    APPLE = "apple"
    GITHUB = "github"
    INVALID = "invalid"

class User(SQLModel, table=True):
    user_id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    email: str = Field(unique=True)
    hashed_password: str = Field(min_length=8)
    is_active: bool
    role: UserRole = Field(default=UserRole.USER)

class OAuthUser(SQLModel, table=True):
    user_id: Optional[uuid.UUID] = Field(foreign_key="user.user_id", index=True)
    provider: ThirdPartyProvider = Field(default=ThirdPartyProvider.INVALID)
    identifier: str = Field(index=True)

    __table_args__ = (
        PrimaryKeyConstraint(
            "provider", "identifier"
        ),
    )
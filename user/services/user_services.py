from typing import Annotated, Dict, Optional
from fastapi import Depends

from config.exceptions import UserAlreadyExists
from user.schemas.sign_up_dto import SignUpDTO
from user.models import User
from sqlmodel import Session, select
from passlib.context import CryptContext
from config.dependencies import get_database_session
from fastapi import logger


async def get_password_context():
    return CryptContext(schemes=["md5_crypt"], deprecated="auto")

class UserService:

    async def create_user(
            self,
            register_data: Dict,
            password_context: CryptContext = Annotated[CryptContext, Depends(get_password_context)],
            database_session: Session = Annotated[Session, Depends(get_database_session)]
    ):
        """
        사용자 생성 시 사용하는 함수
        """
        email: str = register_data.get("email")
        password: str = register_data.get("password")
        await self.email_validate(email=email)
        await self.password_validate(password=password)
        hashed_password: str = await self.get_password_hash(plain_password=password, password_context=password_context)

        # DB에 사용자 정보 저장
        statement = select(User).where(User.email == email)
        _user: Optional[User] = database_session.exec(statement).first()
        if _user is not None:
            raise UserAlreadyExists("User already exists that using this email")

        valid_user: User = User(email=email, hashed_password=hashed_password, is_active=True, role="user")
        database_session.add(valid_user)
        database_session.commit()
        logger.debug("Successfully created user")

    @staticmethod
    async def get_password_hash(plain_password: str, password_context: CryptContext) -> str:
        """
        평문 비밀번호를 Hash화 해주는 함수
        """
        return password_context.hash(plain_password)

    @staticmethod
    async def email_validate(email: str):
        pass

    @staticmethod
    async def password_validate(password: str):
        pass

    @staticmethod
    async def password_verify(plain_password: str, hashed_password: str, password_context: CryptContext) -> bool:
        """
        패스워드가 올바른지 검증하는 함수
        """
        return password_context.verify(plain_password, hashed_password)
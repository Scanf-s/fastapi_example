from config.dependencies import get_database_session
from fastapi import Depends
from sqlmodel import Session, select
from typing import Annotated, Optional
from config.dependencies import get_database_session
from user.services.user_services import UserService, get_user_service
from user.models import User
from config.exceptions import CannotFoundObject
from passlib.context import CryptContext
from user.dependencies import get_password_context


class AuthService:

    async def login(
            self, 
            email: str, 
            password: str,
            user_service: UserService = Annotated[UserService, Depends(get_user_service)],
            database_session: Session = Annotated[Session, Depends(get_database_session)],
            password_context: CryptContext = Annotated[CryptContext, Depends(get_password_context)]
    ):
        await user_service.email_validate(email=email)

        statement = select(User).where(User.email == email)
        _user: Optional[User] = database_session.exec(statement).first()
        if _user is None:
            raise CannotFoundObject("User not found")
        
        await user_service.password_validate(password=password)
        if not await user_service.password_verify(plain_password=password, hashed_password=_user.hashed_password, password_context=password_context):
            raise CannotFoundObject("Password is incorrect")

    async def logout(self, token: str):
        pass
    
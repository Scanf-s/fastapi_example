from typing import Dict, Any, Optional, Annotated
from sqlmodel import Session, select
import jwt
from jwt.exceptions import InvalidTokenError, DecodeError
import uuid

from config.dependencies import get_fastapi_config, get_database_session
from config.settings import Config
from jwt_token.models import Token, TokenType
from user.models import User
from fastapi.logger import logger
from fastapi import Depends
from datetime import datetime, timedelta
from config.exceptions import ObjectNotFound

class TokenService:

    @staticmethod
    async def save_refresh_token(user_id: uuid.UUID, token: str, database_session: Session = None):
        """
        Refresh token 저장 함수

        1. USER 정보 탐색
        2. USER에 할당된 Refresh token 탐색
        3. 만약 Refresh token이 존재한다면 업데이트하고, 없다면 새로 생성
        """
        statement = select(User).where(User.user_id == user_id)
        _user: Optional[User] = database_session.exec(statement).first()
        if _user is None:
            raise ObjectNotFound("Cannot found user while saving refresh token")

        statement = select(Token).where(Token.user_id == _user.user_id)
        logger.debug(statement)
        _token: Optional[Token] = database_session.exec(statement).first()
        logger.debug(_token)

        if _token is None:
            _token = Token(user_id=_user.user_id, token=token, type=TokenType.REFRESH)
        else:
            _token.token = token

        database_session.add(_token)
        database_session.commit()
        logger.debug("Refresh token saved")

    async def create_token(
            self,
            user_id: uuid.UUID,
            token_type: str,
            fastapi_config: Config = Annotated[Config, Depends(get_fastapi_config)],
            database_session: Session = Annotated[Session, Depends(get_database_session)]
    ) -> str:
        """
        토큰 생성 함수
        """
        if token_type not in [TokenType.ACCESS, TokenType.REFRESH]:
            raise ValueError("Invalid token type")

        current_time: datetime = datetime.now()
        expire_time: datetime = current_time

        if token_type == TokenType.ACCESS:
            expire_time = current_time + timedelta(minutes=fastapi_config.ACCESS_TOKEN_EXPIRE_MINUTES)
        elif token_type == TokenType.REFRESH:
            expire_time = current_time + timedelta(days=fastapi_config.REFRESH_TOKEN_EXPIRE_DAYS)

        # JWT Payload 구조 설정
        payload: Dict[str, Any] = {
            "user_id": str(user_id),
            "iat": current_time,
            "exp": expire_time
        }

        # Token 발급
        token: str = jwt.encode(
            payload, fastapi_config.JWT_SECRET, algorithm=fastapi_config.JWT_ALGORITHM
        )
        if token_type == TokenType.REFRESH:
            await self.save_refresh_token(user_id=user_id, token=token, database_session=database_session)

        return token

    @staticmethod
    async def validate_token(token: str, fastapi_config: Config = Annotated[Config, Depends(get_fastapi_config)]) -> bool:
        try:
            jwt.decode(token, fastapi_config.JWT_SECRET, algorithm=fastapi_config.JWT_ALGORITHM)
            return True
        except (InvalidTokenError, DecodeError):
            return False



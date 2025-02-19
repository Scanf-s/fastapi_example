from typing import Dict, Any, Optional
from sqlmodel import Session, select
import jwt
from jwt.exceptions import InvalidTokenError, DecodeError
import uuid
from src.token.models import Token, TokenType
from src.user.models import User
from src.main import fastapi_settings
from src.database import Database
from fastapi.logger import logger
from datetime import datetime, timedelta
from src.exceptions import CannotFoundObject

class TokenService:

    @staticmethod
    def save_refresh_token(user_id: uuid.UUID, token: str):
        """
        Refresh token 저장 함수

        1. USER 정보 탐색
        2. USER에 할당된 Refresh token 탐색
        3. 만약 Refresh token이 존재한다면 업데이트하고, 없다면 새로 생성
        """
        with Session(Database.get_engine()) as session:
            _user: Optional[User] = session.get(User, user_id)
            if _user is None:
                raise CannotFoundObject("Cannot found user while saving refresh token")

            statement = select(Token).where(Token.user_id == _user.user_id)
            _token: Optional[Token] = session.exec(statement).first()

            if _token is None:
                _token = Token(user_id=_user.user_id, token=token, type=TokenType.REFRESH)
            else:
                _token.token = token

            session.add(_token)
            session.commit()
            logger.debug("Refresh token saved")

    def create_token(self, user_id: uuid.UUID, token_type: str) -> str:
        """
        토큰 생성 함수
        """
        if token_type not in [TokenType.ACCESS, TokenType.REFRESH]:
            raise ValueError("Invalid token type")

        current_time: datetime = datetime.now()
        expire_time: datetime = current_time

        if token_type == TokenType.ACCESS:
            expire_time = current_time + timedelta(minutes=fastapi_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        elif token_type == TokenType.REFRESH:
            expire_time = current_time + timedelta(days=fastapi_settings.REFRESH_TOKEN_EXPIRE_DAYS)

        # JWT Payload 구조 설정
        payload: Dict[str, Any] = {
            "user_id": str(user_id),
            "iat": current_time,
            "exp": expire_time
        }

        # Token 발급
        token: str = jwt.encode(
            payload, fastapi_settings.JWT_SECRET, algorithm=fastapi_settings.JWT_ALGORITHM
        )
        if token_type == TokenType.REFRESH:
            self.save_refresh_token(user_id=user_id, token=token)

        return token

    def validate_token(self, token: str) -> bool:
        try:
            jwt.decode(token, fastapi_settings.JWT_SECRET, algorithm=fastapi_settings.JWT_ALGORITHM)
            return True
        except (InvalidTokenError, DecodeError) as e:
            return False



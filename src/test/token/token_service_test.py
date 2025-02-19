from typing import Optional

from sqlmodel import Session, select, create_engine, SQLModel
from fastapi.testclient import TestClient
from fastapi import Depends

from src.main import app
from src.user.models import User
from src.token.models import Token, TokenType
from src.token.services import TokenService

# 테스트용 인메모리 SQLite 엔진
TEST_ENGINE = create_engine(
    "sqlite:///:memory:",
    echo=True,
    connect_args={"check_same_thread": False}
)
SQLModel.metadata.create_all(TEST_ENGINE)

# Database.get_engine()을 테스트 엔진으로 오버라이드
from src.database import Database
Database._engine = TEST_ENGINE

client = TestClient(app)

def test_save_token():
    with Session(TEST_ENGINE) as session:
        # 테스트 사용자 생성 및 저장
        temp_user: User = User(
            email="test@test.com",
            password="test",
            is_active=True,
            role="user"
        )
        session.add(temp_user)
        session.commit()
        session.refresh(temp_user)

    # TokenService의 save_refresh_token 호출
    TokenService.save_refresh_token(user_id=temp_user.user_id, token="test")

    # 저장된 토큰 조회
    with Session(TEST_ENGINE) as session:
        statement = select(Token).where(Token.user_id == temp_user.user_id)
        saved_token: Optional[Token] = session.exec(statement).first()

    assert saved_token is not None, "Token is not saved"
    assert saved_token.token == "test", "Invalid token data"


def test_create_token():
    with Session(TEST_ENGINE) as session:
        # 테스트 사용자 생성 및 저장
        temp_user: User = User(
            email="test@test.com",
            password="test",
            is_active=True,
            role="user"
        )
        session.add(temp_user)
        session.commit()
        session.refresh(temp_user)

    # ACCESS TOKEN 생성 -> TokenService의 create_token 호출
    token_service: TokenService = TokenService()
    access_token: str = token_service.create_token(user_id=temp_user.user_id, token_type=TokenType.ACCESS)

    # Database에 Accesstoken이 저장되어서는 안됨
    statement = select(Token).where(Token.user_id == temp_user.user_id)
    saved_token: Optional[Token] = session.exec(statement).first()
    assert saved_token is None

    # Accesstoken 확인
    assert access_token is not None, "Access token has not generated"
    assert access_token != "", "Invalid access token"

    # REFRESH TOKEN 생성 -> TokenService의 create_token 호출
    refresh_token: str = token_service.create_token(user_id=temp_user.user_id, token_type=TokenType.REFRESH)

    # Database에 RefreshToken이 저장되었는지 확인
    statement = select(Token).where(Token.user_id == temp_user.user_id)
    saved_token: Optional[Token] = session.exec(statement).first()
    assert saved_token is not None
    assert saved_token.token == refresh_token

    # RefreshToken 확인
    assert refresh_token is not None, "Refresh token has not generated"
    assert refresh_token != "", "Invalid refresh token"

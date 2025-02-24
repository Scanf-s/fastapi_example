from typing import Optional

import pytest
from sqlmodel import select
from config.settings import config
from user.models import User
from jwt_token.models import Token, TokenType
from jwt_token.services import TokenService
from test.conftest import database_session          # 테스트 전용 데이터베이스 Pytest fixture


@pytest.mark.asyncio
async def test_save_token(database_session):
    # 테스트 사용자 생성 및 저장
    temp_user: User = User(
        email="test@test.com",
        hashed_password="test",
        is_active=True,
        role="user"
    )
    database_session.add(temp_user)
    database_session.commit()
    database_session.refresh(temp_user)

    # TokenService의 save_refresh_token 호출
    await TokenService.save_refresh_token(user_id=temp_user.user_id, token="test", database_session=database_session)

    # 저장된 토큰 조회
    statement = select(Token).where(Token.user_id == temp_user.user_id)
    saved_token: Optional[Token] = database_session.exec(statement).first()

    assert saved_token is not None, "Token is not saved"
    assert saved_token.token == "test", "Invalid token data"


@pytest.mark.asyncio
async def test_create_token(database_session):
    # 테스트 사용자 생성 및 저장
    temp_user: User = User(
        email="test@test.com",
        hashed_password="test",
        is_active=True,
        role="user"
    )
    database_session.add(temp_user)
    database_session.commit()
    database_session.refresh(temp_user)

    # ACCESS TOKEN 생성 -> TokenService의 create_token 호출
    token_service: TokenService = TokenService()
    access_token: str = await token_service.create_token(
        user_id=temp_user.user_id,
        token_type=TokenType.ACCESS,
        fastapi_config=config,
        database_session=database_session
    )

    # Database에 Accesstoken이 저장되어서는 안됨
    statement = select(Token).where(Token.user_id == temp_user.user_id)
    saved_token: Optional[Token] = database_session.exec(statement).first()
    assert saved_token is None

    # Accesstoken 확인
    assert access_token is not None, "Access token has not generated"
    assert access_token != "", "Invalid access token"

    # REFRESH TOKEN 생성 -> TokenService의 create_token 호출
    refresh_token: str = await token_service.create_token(
        user_id=temp_user.user_id,
        token_type=TokenType.REFRESH,
        fastapi_config=config,
        database_session=database_session
    )

    # Database에 RefreshToken이 저장되었는지 확인
    statement = select(Token).where(Token.user_id == temp_user.user_id)
    saved_token: Optional[Token] = database_session.exec(statement).first()
    assert saved_token is not None
    assert saved_token.token == refresh_token

    # RefreshToken 확인
    assert refresh_token is not None, "Refresh token has not generated"
    assert refresh_token != "", "Invalid refresh token"

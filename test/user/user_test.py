import pytest
from fastapi.testclient import TestClient
from typing import TYPE_CHECKING
from sqlmodel import select
from user.models import User
from user.dependencies import user_dependencies
from test.conftest import database_session          # 테스트 전용 데이터베이스 Pytest fixture
from sqlmodel import Session

if TYPE_CHECKING:
    from user.services.user_services import UserService
    from passlib.context import CryptContext


@pytest.mark.asyncio
async def test_signup_module(database_session):
    # 테스트 사용자 생성
    register_data = {
        "email": "asdf@asdf.com",
        "password": "asdjfijoajf@!I(**kdhkf"
    }

    user_service: UserService = await user_dependencies.get_user_service()
    password_context: CryptContext = await user_dependencies.get_password_context()
    created_user: User = await user_service.create_user(
        register_data=register_data,
        password_context=password_context,
        database_session=database_session
    )
    assert created_user is not None, "User is not created"

    statement = select(User).where(User.email == register_data["email"])
    searched_user: User = database_session.exec(statement).first()
    assert searched_user is not None, "User is not saved in database"
    assert searched_user.email == created_user.email, "created user and searched user is not same"

    print(searched_user.model_dump())


@pytest.mark.asyncio
async def test_signup_request(test_client: TestClient, database_session: Session):

    # Given
    request_data = {
        "email": "asdf@asdf.com",
        "password": "asdjfgaiejfo@124"
    }

    # When
    response = test_client.post(
        url="/api/v1/user",
        json=request_data
    )

    # Then
    assert response.status_code == 201
    statement = select(User).where(User.email == request_data["email"])
    user = database_session.exec(statement).first()
    assert user is not None, "User is not created"
    assert user.email == request_data["email"], "Email is not matched"

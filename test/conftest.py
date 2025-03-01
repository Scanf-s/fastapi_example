import pytest
from sqlmodel import create_engine, SQLModel, Session
from config.dependencies import get_database_session
from fastapi.testclient import TestClient
from main import app
from sqlmodel.pool import StaticPool

"""
데이터베이스를 테스트마다 새로 생성 및 자동으로 초기화하기 위해
Pytest fixture를 사용하여 Database Engine 및 세션 관리
"""
@pytest.fixture(scope="function")
def database_session():
    """
    test_engine을 사용해서 세션을 만들어 테스트에 주입
    """
    engine = create_engine(
        "sqlite://",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass = StaticPool # 인메모리 DB를 여러 쓰레드나 연결에서 공유하기 위해 설정
    )

    from user.models import User
    from jwt_token.models import Token

    # 테스트 테이블 생성
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # 테스트 테이블 정리
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def test_client(database_session: Session):
    """
    테스트 데이터베이스를 사용하도록 FastAPI Client 설정
    """
    def override_get_database_session():
        return database_session

    app.dependency_overrides[get_database_session] = override_get_database_session

    client = TestClient(app)
    yield client

    # 테스트 후 의존성 오버라이드 제거
    app.dependency_overrides.clear()

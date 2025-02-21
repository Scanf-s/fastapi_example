import pytest
from sqlmodel import create_engine, SQLModel, Session

"""
데이터베이스를 테스트마다 새로 생성 및 자동으로 초기화하기 위해
Pytest fixture를 사용하여 Database Engine 및 세션 관리
"""

@pytest.fixture(scope="function")
def test_engine():
    """
    각 테스트 함수마다 새로운 in-memory SQLite 엔진을 생성해서 사용.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)

    # 테스트 테이블 생성
    SQLModel.metadata.create_all(engine)

    yield engine

    # 테스트 테이블 정리
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def database_session(test_engine):
    """
    test_engine을 사용해서 세션을 만들어 테스트에 주입
    """
    with Session(test_engine) as session:
        yield session
        # 세션 close (with 블록 빠져나오며 자동 정리)
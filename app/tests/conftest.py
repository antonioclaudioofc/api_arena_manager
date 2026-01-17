from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from app.core.config import DATABASE_TEST_URL
from sqlalchemy.orm import sessionmaker

from app.modules.auth.dependencies import get_user_repository
from app.shared.repositories.user_repository import UserRepository
from app.main import app
from app.core.database import Base

engine = create_engine(
    DATABASE_TEST_URL,
    connect_args={
        "check_same_thread": False
    }
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db):
    def override_get_user_repository():
        return UserRepository(db)

    app.dependency_overrides[get_user_repository] = override_get_user_repository

    with TestClient(app) as c:
        yield c

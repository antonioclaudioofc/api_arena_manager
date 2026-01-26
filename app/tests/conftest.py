from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from app.core.config import DATABASE_TEST_URL
from sqlalchemy.orm import sessionmaker

from app.modules.auth.dependencies import get_user_repository
from app.shared.repositories.user_repository import UserRepository
from app.main import app
from app.core.database import Base
from app.core.database import get_db

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


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

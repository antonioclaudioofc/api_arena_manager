import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.main import app
from app.dependencies import get_db

load_dotenv()

DATABASE_TEST_URL = os.getenv("DATABASE_TEST_URL")

engine = create_engine(
    DATABASE_TEST_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
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


@pytest.fixture
def create_user(client):
    def _create_user(**overrides):
        payload = {
            "email": "user@example.com",
            "username": "user",
            "first_name": "Teste",
            "last_name": "User",
            "password": "123456"
        }

        payload.update(overrides)

        response = client.post("/auth", json=payload)

        assert response.status_code == 201

        return payload

    return _create_user


@pytest.fixture
def auth_headers(client, create_user):
    user = create_user()

    response = client.post("/auth/token", data={
        "username": user["username"],
        "password": "123456"
    })

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

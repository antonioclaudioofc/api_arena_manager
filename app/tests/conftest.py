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
def client_user(client):
    payload = {
        "email": "user@example.com",
        "username": "user",
        "first_name": "Teste",
        "last_name": "User",
        "password": "123456",
        "role": "client"
    }

    client.post("/auth", json=payload)

    return payload


@pytest.fixture
def admin_user(client):

    payload = {
        "email": "admin@example.com",
        "username": "admin",
        "first_name": "Admin",
        "last_name": "Master",
        "password": "123456",
        "role": "admin"
    }

    client.post("/auth", json=payload)

    return payload


@pytest.fixture
def auth_headers(client, client_user):

    response = client.post("/auth/login", data={
        "username": client_user["username"],
        "password": "123456"
    })

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def admin_headers(client, admin_user):

    response = client.post("/auth/login", data={
        "username": admin_user["username"],
        "password": "123456"
    })

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

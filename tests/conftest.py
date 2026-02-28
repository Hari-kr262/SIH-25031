"""Pytest configuration and shared fixtures."""

import os
# Override DATABASE_URL before any app imports so SQLAlchemy uses SQLite
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.database import Base, get_db
from backend.app import create_app

# Use SQLite in-memory for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def db():
    """Create test database and tables."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def client(db):
    """Create test client with DB override."""
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture
def admin_token(client):
    """Register and login a test admin user, return JWT token."""
    # Register
    client.post("/api/v1/auth/register", json={
        "full_name": "Test Admin",
        "email": "testadmin@test.com",
        "password": "testpass123",
        "role": "municipal_admin",
    })
    # Login
    resp = client.post("/api/v1/auth/login", json={
        "email": "testadmin@test.com",
        "password": "testpass123",
    })
    if resp.status_code == 200:
        return resp.json()["access_token"]
    return None


@pytest.fixture
def citizen_token(client):
    """Register and login a test citizen user, return JWT token."""
    client.post("/api/v1/auth/register", json={
        "full_name": "Test Citizen",
        "email": "testcitizen@test.com",
        "password": "testpass123",
        "role": "citizen",
    })
    resp = client.post("/api/v1/auth/login", json={
        "email": "testcitizen@test.com",
        "password": "testpass123",
    })
    if resp.status_code == 200:
        return resp.json()["access_token"]
    return None

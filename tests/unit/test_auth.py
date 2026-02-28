"""Unit tests for authentication service."""

import pytest
from unittest.mock import MagicMock, patch
from backend.utils.security import hash_password, verify_password, create_access_token, decode_token


def test_password_hashing():
    """Test that passwords are correctly hashed and verified."""
    plain = "securepassword123"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_jwt_token_creation_and_decode():
    """Test JWT token creation and decoding."""
    data = {"sub": "123", "role": "citizen", "email": "test@test.com"}
    token = create_access_token(data)
    assert token is not None

    decoded = decode_token(token)
    assert decoded is not None
    assert decoded["sub"] == "123"
    assert decoded["role"] == "citizen"
    assert decoded["type"] == "access"


def test_invalid_token_returns_none():
    """Test that an invalid token returns None."""
    result = decode_token("invalid.token.here")
    assert result is None


def test_expired_token():
    """Test that expired tokens return None."""
    from datetime import timedelta
    data = {"sub": "123"}
    token = create_access_token(data, expires_delta=timedelta(seconds=-1))
    decoded = decode_token(token)
    assert decoded is None


class TestAuthRoutes:
    """Test authentication API routes."""

    def test_register_success(self, client):
        resp = client.post("/api/v1/auth/register", json={
            "full_name": "New User",
            "email": "newuser@test.com",
            "password": "password123",
            "role": "citizen",
        })
        assert resp.status_code == 201
        assert resp.json()["success"] is True

    def test_register_duplicate_email(self, client):
        """Registering with the same email should fail."""
        data = {"full_name": "Dup", "email": "dup@test.com",
                "password": "pass123", "role": "citizen"}
        client.post("/api/v1/auth/register", json=data)
        resp = client.post("/api/v1/auth/register", json=data)
        assert resp.status_code == 409

    def test_login_success(self, client):
        client.post("/api/v1/auth/register", json={
            "full_name": "Login Test", "email": "logintest@test.com",
            "password": "testpass123", "role": "citizen",
        })
        resp = client.post("/api/v1/auth/login", json={
            "email": "logintest@test.com", "password": "testpass123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_login_wrong_password(self, client):
        resp = client.post("/api/v1/auth/login", json={
            "email": "logintest@test.com", "password": "wrongpass",
        })
        assert resp.status_code == 401

    def test_get_profile_authenticated(self, client, citizen_token):
        if not citizen_token:
            pytest.skip("Could not obtain citizen token")
        resp = client.get("/api/v1/auth/me",
                         headers={"Authorization": f"Bearer {citizen_token}"})
        assert resp.status_code == 200

    def test_get_profile_unauthenticated(self, client):
        resp = client.get("/api/v1/auth/me")
        assert resp.status_code == 401

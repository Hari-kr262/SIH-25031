"""Unit tests for issue service and routes."""

import pytest


class TestIssueRoutes:
    """Test issue management endpoints."""

    def test_create_issue_authenticated(self, client, citizen_token):
        if not citizen_token:
            pytest.skip("No citizen token")
        resp = client.post(
            "/api/v1/issues/",
            headers={"Authorization": f"Bearer {citizen_token}"},
            json={
                "title": "Test Pothole",
                "description": "Large pothole on main road",
                "category": "pothole",
                "priority": "high",
            },
        )
        assert resp.status_code == 201
        assert resp.json()["success"] is True

    def test_create_issue_unauthenticated(self, client):
        resp = client.post("/api/v1/issues/", json={"title": "Test", "category": "pothole"})
        assert resp.status_code == 401

    def test_list_issues_public(self, client):
        resp = client.get("/api/v1/issues/")
        assert resp.status_code == 200

    def test_list_issues_with_filter(self, client):
        resp = client.get("/api/v1/issues/?category=pothole&page=1&page_size=5")
        assert resp.status_code == 200

    def test_get_trending_issues(self, client):
        resp = client.get("/api/v1/issues/trending")
        assert resp.status_code == 200

    def test_get_nonexistent_issue(self, client):
        resp = client.get("/api/v1/issues/999999")
        assert resp.status_code == 404

    def test_my_issues_requires_auth(self, client):
        resp = client.get("/api/v1/issues/my")
        assert resp.status_code == 401

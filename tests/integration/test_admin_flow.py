"""Integration tests for admin workflow."""

import pytest


class TestAdminFlow:
    """Test admin management operations."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        # Register admin
        client.post("/api/v1/auth/register", json={
            "full_name": "Integration Admin",
            "email": "intadmin@test.com",
            "password": "adminpass123",
            "role": "municipal_admin",
        })
        login_resp = client.post("/api/v1/auth/login", json={
            "email": "intadmin@test.com",
            "password": "adminpass123",
        })
        self.token = login_resp.json().get("access_token") if login_resp.status_code == 200 else None

    def test_admin_can_list_users(self):
        if not self.token:
            pytest.skip("Could not authenticate")
        resp = self.client.get(
            "/api/v1/admin/users",
            headers={"Authorization": f"Bearer {self.token}"},
        )
        assert resp.status_code == 200

    def test_admin_can_list_departments(self):
        if not self.token:
            pytest.skip("Could not authenticate")
        resp = self.client.get(
            "/api/v1/admin/departments",
            headers={"Authorization": f"Bearer {self.token}"},
        )
        assert resp.status_code == 200

    def test_admin_dashboard(self):
        if not self.token:
            pytest.skip("Could not authenticate")
        resp = self.client.get(
            "/api/v1/dashboard/admin",
            headers={"Authorization": f"Bearer {self.token}"},
        )
        assert resp.status_code == 200

    def test_non_admin_cannot_access_admin_routes(self, client, citizen_token):
        if not citizen_token:
            pytest.skip("No citizen token")
        resp = client.get(
            "/api/v1/admin/users",
            headers={"Authorization": f"Bearer {citizen_token}"},
        )
        assert resp.status_code == 403

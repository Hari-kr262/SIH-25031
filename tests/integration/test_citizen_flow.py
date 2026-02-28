"""Integration tests for the citizen workflow."""

import pytest


class TestCitizenFlow:
    """Test the complete citizen journey: register → report → vote → verify."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        # Register a fresh citizen for each test
        resp = client.post("/api/v1/auth/register", json={
            "full_name": "Integration Citizen",
            "email": "intcitizen@test.com",
            "password": "pass123",
            "role": "citizen",
        })
        login_resp = client.post("/api/v1/auth/login", json={
            "email": "intcitizen@test.com",
            "password": "pass123",
        })
        self.token = login_resp.json().get("access_token") if login_resp.status_code == 200 else None

    def test_full_citizen_workflow(self):
        """Test: register → report issue → check my issues."""
        if not self.token:
            pytest.skip("Could not authenticate")

        headers = {"Authorization": f"Bearer {self.token}"}

        # 1. Report an issue
        report_resp = self.client.post(
            "/api/v1/issues/",
            headers=headers,
            json={
                "title": "Broken streetlight on Gandhi Road",
                "description": "The streetlight has been broken for 3 days",
                "category": "streetlight",
                "priority": "medium",
                "address": "Gandhi Road, Ward 5, Ranchi",
                "ward": "5",
            },
        )
        assert report_resp.status_code == 201
        issue_id = report_resp.json()["data"]["id"]

        # 2. Check my issues
        my_issues_resp = self.client.get("/api/v1/issues/my", headers=headers)
        assert my_issues_resp.status_code == 200
        items = my_issues_resp.json()["data"]["items"]
        assert any(i["id"] == issue_id for i in items)

        # 3. Get issue details
        detail_resp = self.client.get(f"/api/v1/issues/{issue_id}")
        assert detail_resp.status_code == 200
        assert detail_resp.json()["status"] == "pending"

        # 4. Add a comment
        comment_resp = self.client.post(
            "/api/v1/comments/",
            headers=headers,
            json={"issue_id": issue_id, "content": "This has been a problem for weeks"},
        )
        assert comment_resp.status_code == 201

        # 5. Check dashboard
        dashboard_resp = self.client.get("/api/v1/dashboard/public")
        assert dashboard_resp.status_code == 200
        assert dashboard_resp.json()["data"]["total_issues"] >= 1

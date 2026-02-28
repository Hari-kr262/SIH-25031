"""Unit tests for voting service."""

import pytest
from unittest.mock import MagicMock
from backend.services.voting_service import VotingService
from backend.models.vote import VoteType


class TestVotingService:
    """Test VotingService directly."""

    def test_vote_type_enum(self):
        assert VoteType.up == "up"
        assert VoteType.down == "down"


class TestVoteRoutes:
    """Test vote API routes."""

    def test_upvote_requires_auth(self, client):
        resp = client.post("/api/v1/votes/upvote/1")
        assert resp.status_code == 401

    def test_downvote_requires_auth(self, client):
        resp = client.post("/api/v1/votes/downvote/1")
        assert resp.status_code == 401

    def test_vote_nonexistent_issue(self, client, citizen_token):
        if not citizen_token:
            pytest.skip("No citizen token")
        resp = client.post(
            "/api/v1/votes/upvote/999999",
            headers={"Authorization": f"Bearer {citizen_token}"},
        )
        assert resp.status_code == 404

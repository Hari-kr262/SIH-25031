"""Unit tests for gamification service."""

import pytest
from config.constants import get_level_for_points, CITIZEN_LEVELS, Points


def test_level_for_zero_points():
    level = get_level_for_points(0)
    assert level["name"] == "Newcomer"


def test_level_boundaries():
    assert get_level_for_points(50)["name"] == "Newcomer"
    assert get_level_for_points(51)["name"] == "Active Citizen"
    assert get_level_for_points(200)["name"] == "Active Citizen"
    assert get_level_for_points(201)["name"] == "Community Champion"
    assert get_level_for_points(1001)["name"] == "City Hero"


def test_gamification_points_constants():
    assert Points.REPORT_ISSUE == 10
    assert Points.UPVOTE == 2
    assert Points.VERIFY_RESOLUTION == 5
    assert Points.FAKE_PENALTY == -20
    assert Points.VOLUNTEER_FIX == 25


def test_gamification_leaderboard(client):
    resp = client.get("/api/v1/gamification/leaderboard")
    assert resp.status_code == 200


def test_gamification_badges_list(client):
    resp = client.get("/api/v1/gamification/badges")
    assert resp.status_code == 200

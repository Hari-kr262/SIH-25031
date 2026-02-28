"""Unit tests for SLA utilities."""

import pytest
from datetime import datetime, timedelta
from backend.utils.time_utils import calculate_deadline, get_elapsed_percent, is_overdue


def test_calculate_deadline():
    created = datetime(2024, 1, 1, 12, 0, 0)
    deadline = calculate_deadline(created, deadline_hours=48)
    assert deadline == datetime(2024, 1, 3, 12, 0, 0)


def test_elapsed_percent_new_issue():
    created = datetime.utcnow() - timedelta(hours=12)
    deadline = created + timedelta(hours=24)
    pct = get_elapsed_percent(created, deadline)
    assert 40 < pct < 60  # Approx 50%


def test_elapsed_percent_overdue():
    created = datetime(2024, 1, 1)
    deadline = datetime(2024, 1, 2)
    pct = get_elapsed_percent(created, deadline)
    assert pct > 100


def test_is_overdue_past():
    past = datetime(2020, 1, 1)
    assert is_overdue(past) is True


def test_is_overdue_future():
    future = datetime.utcnow() + timedelta(hours=1)
    assert is_overdue(future) is False

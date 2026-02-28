"""Time and SLA utility functions."""

from datetime import datetime, timedelta, UTC
import pytz

IST = pytz.timezone("Asia/Kolkata")


def now_utc() -> datetime:
    """Return current UTC time (timezone-aware)."""
    return datetime.now(UTC)


def now_ist() -> datetime:
    """Return current IST time."""
    return datetime.now(IST)


def utc_to_ist(dt: datetime) -> datetime:
    """Convert UTC datetime to IST."""
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    return dt.astimezone(IST)


def calculate_deadline(created_at: datetime, deadline_hours: int) -> datetime:
    """Calculate SLA deadline from creation time and hours."""
    return created_at + timedelta(hours=deadline_hours)


def get_elapsed_percent(created_at: datetime, deadline: datetime) -> float:
    """Return percentage of SLA time elapsed (0-100+)."""
    total_seconds = (deadline - created_at).total_seconds()
    now = datetime.now(UTC)
    elapsed_seconds = (now - created_at.replace(tzinfo=UTC)).total_seconds()
    if total_seconds <= 0:
        return 100.0
    return round((elapsed_seconds / total_seconds) * 100, 2)


def is_overdue(deadline: datetime) -> bool:
    """Check if a deadline has passed."""
    return datetime.now(UTC) > deadline.replace(tzinfo=UTC)


def format_duration(hours: float) -> str:
    """Format hours into human-readable string."""
    if hours < 1:
        return f"{int(hours * 60)} minutes"
    elif hours < 24:
        return f"{int(hours)} hours"
    else:
        days = int(hours // 24)
        remaining_hours = int(hours % 24)
        if remaining_hours:
            return f"{days} days {remaining_hours} hours"
        return f"{days} days"

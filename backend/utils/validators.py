"""Input validation utilities."""

import re
from typing import Optional


def validate_phone(phone: str) -> bool:
    """Validate Indian phone number format."""
    pattern = r"^(\+91[-\s]?)?[6-9]\d{9}$"
    return bool(re.match(pattern, phone.replace(" ", "").replace("-", "")))


def validate_coordinates(lat: Optional[float], lng: Optional[float]) -> bool:
    """Validate that latitude and longitude are within India's bounds."""
    if lat is None or lng is None:
        return True  # Optional fields
    return 8.0 <= lat <= 37.0 and 68.0 <= lng <= 97.5


def validate_ward(ward: str) -> bool:
    """Basic ward name validation."""
    return bool(ward and len(ward.strip()) > 0)


def sanitize_string(value: str, max_length: int = 500) -> str:
    """Strip HTML tags and limit string length."""
    import html
    clean = html.escape(value.strip())
    return clean[:max_length]

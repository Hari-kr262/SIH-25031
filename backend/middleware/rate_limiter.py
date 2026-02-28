"""Simple in-memory rate limiter using slowapi."""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)


def get_limiter() -> Limiter:
    """Return the application rate limiter instance."""
    return limiter

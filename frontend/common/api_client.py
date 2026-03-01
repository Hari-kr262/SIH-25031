"""Reusable API client for CivicResolve frontend."""
import httpx

BASE_URL = "http://127.0.0.1:8000/api/v1"


def get(endpoint, token=None):
    """Perform a GET request to the API."""
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = httpx.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
    return resp.json()


def post(endpoint, data, token=None):
    """Perform a POST request to the API."""
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = httpx.post(f"{BASE_URL}{endpoint}", json=data, headers=headers, timeout=10)
    return resp


def put(endpoint, data=None, token=None):
    """Perform a PUT request to the API."""
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = httpx.put(f"{BASE_URL}{endpoint}", json=data or {}, headers=headers, timeout=10)
    return resp

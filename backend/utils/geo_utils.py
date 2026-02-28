"""Geographic utility functions."""

import math
from typing import List, Dict, Tuple, Optional


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two points (km)."""
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def find_nearby_issues(
    center_lat: float,
    center_lng: float,
    issues: List[Dict],
    radius_km: float = 1.0,
) -> List[Dict]:
    """Filter issues within a given radius of a center point."""
    nearby = []
    for issue in issues:
        if issue.get("latitude") and issue.get("longitude"):
            dist = haversine_distance(
                center_lat, center_lng, issue["latitude"], issue["longitude"]
            )
            if dist <= radius_km:
                issue["distance_km"] = round(dist, 3)
                nearby.append(issue)
    return sorted(nearby, key=lambda x: x.get("distance_km", 0))


def get_bounding_box(lat: float, lng: float, radius_km: float) -> Tuple[float, float, float, float]:
    """Return (min_lat, max_lat, min_lng, max_lng) bounding box."""
    lat_delta = radius_km / 111.0
    lng_delta = radius_km / (111.0 * math.cos(math.radians(lat)))
    return lat - lat_delta, lat + lat_delta, lng - lng_delta, lng + lng_delta


def reverse_geocode(lat: float, lng: float) -> Optional[str]:
    """Attempt reverse geocoding using geopy (Nominatim)."""
    try:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="civicresolve")
        location = geolocator.reverse((lat, lng), language="en", timeout=5)
        return location.address if location else None
    except Exception:
        return None

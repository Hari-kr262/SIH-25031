"""
Application-wide constants for gamification, SLA, colors, and configuration.
"""

from enum import Enum


# ---------------------------------------------------------------------------
# Color Scheme
# ---------------------------------------------------------------------------
class Colors:
    PRIMARY = "#1565C0"      # Civic Blue
    SUCCESS = "#2E7D32"      # Government Green
    WARNING = "#F57F17"      # Alert Amber
    ERROR = "#C62828"        # Critical Red
    SURFACE = "#F5F5F5"
    BACKGROUND = "#FFFFFF"
    ON_PRIMARY = "#FFFFFF"
    SECONDARY = "#0288D1"


# ---------------------------------------------------------------------------
# Gamification — Points
# ---------------------------------------------------------------------------
class Points:
    REPORT_ISSUE = 10
    ISSUE_VERIFIED = 5
    UPVOTE = 2
    VERIFY_RESOLUTION = 5
    VOLUNTEER_VERIFY = 15
    VOLUNTEER_FIX = 25
    FAKE_PENALTY = -20
    COMMENT = 1
    DAILY_LOGIN = 3


# ---------------------------------------------------------------------------
# Gamification — Levels
# ---------------------------------------------------------------------------
CITIZEN_LEVELS = [
    {"name": "Newcomer",           "min": 0,    "max": 50,   "icon": "🌱"},
    {"name": "Active Citizen",     "min": 51,   "max": 200,  "icon": "👤"},
    {"name": "Community Champion", "min": 201,  "max": 500,  "icon": "🏅"},
    {"name": "Civic Leader",       "min": 501,  "max": 1000, "icon": "🎖️"},
    {"name": "City Hero",          "min": 1001, "max": None, "icon": "🏆"},
]


def get_level_for_points(points: int) -> dict:
    """Return the level dict for a given points total."""
    for level in reversed(CITIZEN_LEVELS):
        if level["min"] <= points:
            return level
    return CITIZEN_LEVELS[0]


# ---------------------------------------------------------------------------
# Gamification — Badges
# ---------------------------------------------------------------------------
BADGE_DEFINITIONS = [
    {
        "name": "First Report",
        "description": "Submitted your very first civic issue",
        "icon": "🎯",
        "points_required": 0,
        "criteria": "reports_count >= 1",
    },
    {
        "name": "Active Reporter",
        "description": "Submitted 10 or more issues",
        "icon": "📣",
        "points_required": 50,
        "criteria": "reports_count >= 10",
    },
    {
        "name": "Top Reporter",
        "description": "Submitted 50 or more issues",
        "icon": "🏆",
        "points_required": 200,
        "criteria": "reports_count >= 50",
    },
    {
        "name": "Trusted Verifier",
        "description": "Verified 20 or more issue resolutions",
        "icon": "✅",
        "points_required": 100,
        "criteria": "verifications_count >= 20",
    },
    {
        "name": "Community Hero",
        "description": "Earned 100 or more points",
        "icon": "🦸",
        "points_required": 100,
        "criteria": "total_points >= 100",
    },
    {
        "name": "Star Citizen",
        "description": "Top contributor this month",
        "icon": "⭐",
        "points_required": 500,
        "criteria": "monthly_top_contributor",
    },
    {
        "name": "Guardian",
        "description": "Reported 5 or more fake issues correctly",
        "icon": "🛡️",
        "points_required": 0,
        "criteria": "fake_reports_found >= 5",
    },
    {
        "name": "Legend",
        "description": "Earned 1000 or more points",
        "icon": "👑",
        "points_required": 1000,
        "criteria": "total_points >= 1000",
    },
]


# ---------------------------------------------------------------------------
# SLA Defaults (hours)
# ---------------------------------------------------------------------------
SLA_DEFAULTS = {
    "pothole":          {"deadline_hours": 48,  "warning_threshold_percent": 75},
    "garbage":          {"deadline_hours": 24,  "warning_threshold_percent": 75},
    "streetlight":      {"deadline_hours": 72,  "warning_threshold_percent": 75},
    "water_leak":       {"deadline_hours": 12,  "warning_threshold_percent": 80},
    "drainage":         {"deadline_hours": 48,  "warning_threshold_percent": 75},
    "road_damage":      {"deadline_hours": 72,  "warning_threshold_percent": 75},
    "illegal_dumping":  {"deadline_hours": 24,  "warning_threshold_percent": 75},
    "fallen_tree":      {"deadline_hours": 6,   "warning_threshold_percent": 80},
    "sewage":           {"deadline_hours": 12,  "warning_threshold_percent": 80},
    "public_property":  {"deadline_hours": 96,  "warning_threshold_percent": 70},
    "other":            {"deadline_hours": 72,  "warning_threshold_percent": 75},
}


# ---------------------------------------------------------------------------
# Department Names
# ---------------------------------------------------------------------------
DEPARTMENTS = [
    {"name": "Roads & Infrastructure",  "description": "Potholes, road damage, pavements"},
    {"name": "Water & Sanitation",      "description": "Water leaks, sewage, drainage"},
    {"name": "Solid Waste Management",  "description": "Garbage collection, illegal dumping"},
    {"name": "Electricity",             "description": "Streetlights, electrical issues"},
    {"name": "Drainage",                "description": "Stormwater drains, flooding"},
    {"name": "Parks & Recreation",      "description": "Parks, trees, public spaces"},
    {"name": "Public Health",           "description": "Health hazards, pest control"},
    {"name": "Public Property",         "description": "Government buildings, public assets"},
]


# ---------------------------------------------------------------------------
# Issue Category → Department Mapping
# ---------------------------------------------------------------------------
CATEGORY_TO_DEPARTMENT = {
    "pothole":          "Roads & Infrastructure",
    "road_damage":      "Roads & Infrastructure",
    "streetlight":      "Electricity",
    "water_leak":       "Water & Sanitation",
    "sewage":           "Water & Sanitation",
    "garbage":          "Solid Waste Management",
    "illegal_dumping":  "Solid Waste Management",
    "drainage":         "Drainage",
    "fallen_tree":      "Parks & Recreation",
    "public_property":  "Public Property",
    "other":            "Public Property",
}


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


# ---------------------------------------------------------------------------
# File Upload Limits
# ---------------------------------------------------------------------------
MAX_IMAGE_SIZE_MB = 10
MAX_VIDEO_SIZE_MB = 100
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]
ALLOWED_VIDEO_TYPES = ["video/mp4", "video/mpeg", "video/quicktime", "video/webm"]
ALLOWED_DOCUMENT_TYPES = ["application/pdf", "application/msword",
                           "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]


# ---------------------------------------------------------------------------
# Volunteer vote weight
# ---------------------------------------------------------------------------
TRUSTED_VOLUNTEER_VOTE_WEIGHT = 2
REGULAR_VOTE_WEIGHT = 1

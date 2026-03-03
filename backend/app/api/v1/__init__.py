"""
API v1 routes
"""

from app.api.v1 import (
    auth,
    users,
    subjects,
    sessions,
    goals,
    deadlines,
    wellness,
    analytics,
    ai
)

__all__ = [
    "auth",
    "users",
    "subjects",
    "sessions",
    "goals",
    "deadlines",
    "wellness",
    "analytics",
    "ai",
]

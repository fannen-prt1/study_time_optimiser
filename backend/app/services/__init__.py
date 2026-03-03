"""
Business logic services
"""

from app.services.auth_service import AuthService
from app.services.auth_dependencies import (
    get_current_user,
    get_current_verified_user,
    get_optional_current_user
)
from app.services.subject_service import SubjectService
from app.services.study_session_service import StudySessionService
from app.services.goal_service import GoalService
from app.services.deadline_service import DeadlineService
from app.services.wellness_service import WellnessService
from app.services.user_service import UserService
from app.services.analytics_service import AnalyticsService

__all__ = [
    "AuthService",
    "get_current_user",
    "get_current_verified_user",
    "get_optional_current_user",
    "SubjectService",
    "StudySessionService",
    "GoalService",
    "DeadlineService",
    "WellnessService",
    "UserService",
    "AnalyticsService",
]

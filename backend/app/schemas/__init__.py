"""
Pydantic schemas for request/response validation
"""

# User schemas
from app.schemas.user import (
    UserBase, UserCreate, UserUpdate, UserResponse, UserInDB,
    PasswordChange, PasswordResetRequest, PasswordReset, StudentType
)

# Auth schemas
from app.schemas.auth import (
    LoginRequest, TokenResponse, TokenRefreshRequest,
    TokenData, EmailVerificationRequest
)

# Subject schemas
from app.schemas.subject import (
    SubjectBase, SubjectCreate, SubjectUpdate, SubjectResponse
)

# Study Session schemas
from app.schemas.study_session import (
    StudySessionBase, StudySessionCreate, StudySessionUpdate,
    StudySessionComplete, StudySessionResponse, SessionType, SessionStatus
)

# Goal schemas
from app.schemas.goal import (
    GoalBase, GoalCreate, GoalUpdate, GoalResponse, GoalType
)

# Deadline schemas
from app.schemas.deadline import (
    DeadlineBase, DeadlineCreate, DeadlineUpdate, DeadlineResponse, PriorityLevel
)

# Daily Wellness schemas
from app.schemas.daily_wellness import (
    DailyWellnessBase, DailyWellnessCreate, DailyWellnessUpdate, DailyWellnessResponse
)

# Analytics schemas
from app.schemas.analytics import (
    AnalyticsRequest,
    StudyTimeStats,
    SubjectStats,
    ProductivityTrend,
    GoalProgress,
    StreakInfo,
    WellnessCorrelation,
    DashboardAnalytics,
    TimeRange
)

__all__ = [
    # User
    "UserBase", "UserCreate", "UserUpdate", "UserResponse", "UserInDB",
    "PasswordChange", "PasswordResetRequest", "PasswordReset", "StudentType",
    # Auth
    "LoginRequest", "TokenResponse", "TokenRefreshRequest",
    "TokenData", "EmailVerificationRequest",
    # Subject
    "SubjectBase", "SubjectCreate", "SubjectUpdate", "SubjectResponse",
    # Study Session
    "StudySessionBase", "StudySessionCreate", "StudySessionUpdate",
    "StudySessionComplete", "StudySessionResponse", "SessionType", "SessionStatus",
    # Goal
    "GoalBase", "GoalCreate", "GoalUpdate", "GoalResponse", "GoalType",
    # Deadline
    "DeadlineBase", "DeadlineCreate", "DeadlineUpdate", "DeadlineResponse", "PriorityLevel",
    # Wellness
    "DailyWellnessBase", "DailyWellnessCreate", "DailyWellnessUpdate", "DailyWellnessResponse",
    # Analytics
    "AnalyticsRequest", "StudyTimeStats", "SubjectStats",
    "ProductivityTrend", "GoalProgress", "StreakInfo", "WellnessCorrelation",
    "DashboardAnalytics", "TimeRange",
]

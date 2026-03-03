"""
Analytics Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Tuple
from datetime import date, datetime
from enum import Enum


class TimeRange(str, Enum):
    """Time range for analytics"""
    TODAY = "today"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    CUSTOM = "custom"


class AnalyticsRequest(BaseModel):
    """Schema for analytics request"""
    time_range: TimeRange = TimeRange.WEEK
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    subject_id: Optional[str] = None


class StudyTimeStats(BaseModel):
    """Study time statistics"""
    total_minutes: int
    total_sessions: int
    average_session_minutes: float
    total_planned_minutes: int
    completion_rate: float
    average_productivity_score: float
    average_focus_score: float


class SubjectStats(BaseModel):
    """Statistics per subject"""
    subject_id: str
    subject_name: str
    subject_color: str
    subject_icon: Optional[str] = None
    total_sessions: int
    total_minutes: int
    average_productivity: float


class ProductivityTrend(BaseModel):
    """Productivity trend over time"""
    date: date
    total_minutes: int
    session_count: int
    average_productivity: float
    average_focus: float


class GoalProgress(BaseModel):
    """Goal progress summary"""
    goal_id: str
    title: str
    subject_name: str
    goal_type: str
    current_value: float
    target_value: float
    progress_percentage: float
    is_achieved: bool
    days_remaining: Optional[int] = None
    target_date: Optional[date] = None


class StreakInfo(BaseModel):
    """Study streak information"""
    current_streak: int
    longest_streak: int
    last_study_date: Optional[date] = None
    total_study_days: int = 0


class WellnessCorrelation(BaseModel):
    """Correlation between wellness and productivity"""
    average_sleep_hours: float
    average_productivity: float
    high_productivity_sleep_average: float
    low_productivity_sleep_average: float
    optimal_sleep_range: Tuple[int, int]
    energy_productivity_correlation: str


class DashboardAnalytics(BaseModel):
    """Complete dashboard analytics"""
    study_time_stats: StudyTimeStats
    subject_stats: List[SubjectStats]
    productivity_trends: List[ProductivityTrend]
    goal_progress: List[GoalProgress]
    streak_info: StreakInfo
    wellness_correlation: WellnessCorrelation
    upcoming_deadlines: List[Dict[str, Any]]

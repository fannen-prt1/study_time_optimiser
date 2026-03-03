from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.database.dependencies import get_db
from app.services.auth_dependencies import get_current_verified_user
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import (
    StudyTimeStats,
    SubjectStats,
    ProductivityTrend,
    GoalProgress,
    StreakInfo,
    WellnessCorrelation,
    DashboardAnalytics
)
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/dashboard", response_model=DashboardAnalytics)
def get_dashboard_analytics(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard analytics"""
    return AnalyticsService.get_dashboard_analytics(db, current_user.id, days)


@router.get("/study-time", response_model=StudyTimeStats)
def get_study_time_stats(
    start_date: Optional[date] = Query(None, description="Start date for analysis"),
    end_date: Optional[date] = Query(None, description="End date for analysis"),
    subject_id: Optional[UUID] = Query(None, description="Filter by subject"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get study time statistics"""
    # Default to last 30 days if not specified
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()
    
    return AnalyticsService.get_study_time_stats(
        db, current_user.id, start_date, end_date, subject_id
    )


@router.get("/subjects", response_model=list[SubjectStats])
def get_subject_stats(
    start_date: Optional[date] = Query(None, description="Start date for analysis"),
    end_date: Optional[date] = Query(None, description="End date for analysis"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get statistics per subject"""
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()
    
    return AnalyticsService.get_subject_stats(db, current_user.id, start_date, end_date)


@router.get("/productivity-trends", response_model=list[ProductivityTrend])
def get_productivity_trends(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get daily productivity trends"""
    return AnalyticsService.get_productivity_trends(db, current_user.id, days)


@router.get("/goals/progress", response_model=list[GoalProgress])
def get_goal_progress(
    subject_id: Optional[UUID] = Query(None, description="Filter by subject"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get progress for all active goals"""
    return AnalyticsService.get_goal_progress(db, current_user.id, subject_id)


@router.get("/streak", response_model=StreakInfo)
def get_streak_info(
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get study streak information"""
    return AnalyticsService.get_streak_info(db, current_user.id)


@router.get("/wellness-correlation", response_model=WellnessCorrelation)
def get_wellness_correlation(
    days: int = Query(30, ge=7, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Analyze correlation between wellness metrics and productivity"""
    return AnalyticsService.get_wellness_correlation(db, current_user.id, days)

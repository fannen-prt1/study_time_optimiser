from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, case
from datetime import datetime, date, timedelta
from collections import defaultdict

from app.models.study_session import StudySession
from app.models.subject import Subject
from app.models.goal import Goal
from app.models.deadline import Deadline
from app.models.daily_wellness import DailyWellness
from app.models.study_streak import StudyStreak
from app.schemas.analytics import (
    StudyTimeStats,
    SubjectStats,
    ProductivityTrend,
    GoalProgress,
    StreakInfo,
    WellnessCorrelation,
    DashboardAnalytics
)


class AnalyticsService:
    """Service for analytics and insights"""
    
    @staticmethod
    def get_study_time_stats(
        db: Session,
        user_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        subject_id: Optional[UUID] = None
    ) -> StudyTimeStats:
        """Get study time statistics"""
        query = db.query(StudySession).filter(
            and_(
                StudySession.user_id == user_id,
                StudySession.status == "completed"
            )
        )
        
        if start_date:
            query = query.filter(StudySession.start_time >= datetime.combine(start_date, datetime.min.time()))
        
        if end_date:
            query = query.filter(StudySession.start_time <= datetime.combine(end_date, datetime.max.time()))
        
        if subject_id:
            query = query.filter(StudySession.subject_id == subject_id)
        
        sessions = query.all()
        
        if not sessions:
            return StudyTimeStats(
                total_minutes=0,
                total_sessions=0,
                average_session_minutes=0,
                total_planned_minutes=0,
                completion_rate=0,
                average_productivity_score=0,
                average_focus_score=0
            )
        
        total_actual = sum(s.actual_duration_minutes or 0 for s in sessions)
        total_planned = sum(s.planned_duration_minutes or 0 for s in sessions)
        total_sessions = len(sessions)
        
        # Calculate averages for sessions with scores
        sessions_with_productivity = [s for s in sessions if s.productivity_score is not None]
        sessions_with_focus = [s for s in sessions if s.focus_score is not None]
        
        avg_productivity = (
            sum(s.productivity_score for s in sessions_with_productivity) / len(sessions_with_productivity)
            if sessions_with_productivity else 0
        )
        
        avg_focus = (
            sum(s.focus_score for s in sessions_with_focus) / len(sessions_with_focus)
            if sessions_with_focus else 0
        )
        
        completion_rate = (total_actual / total_planned * 100) if total_planned > 0 else 0
        
        return StudyTimeStats(
            total_minutes=total_actual,
            total_sessions=total_sessions,
            average_session_minutes=total_actual / total_sessions if total_sessions > 0 else 0,
            total_planned_minutes=total_planned,
            completion_rate=round(completion_rate, 2),
            average_productivity_score=round(avg_productivity, 2),
            average_focus_score=round(avg_focus, 2)
        )
    
    @staticmethod
    def get_subject_stats(
        db: Session,
        user_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[SubjectStats]:
        """Get statistics per subject"""
        query = db.query(
            Subject.id,
            Subject.name,
            Subject.color,
            Subject.icon,
            func.count(StudySession.id).label('session_count'),
            func.sum(StudySession.actual_duration_minutes).label('total_minutes'),
            func.avg(StudySession.productivity_score).label('avg_productivity')
        ).join(
            StudySession,
            and_(
                StudySession.subject_id == Subject.id,
                StudySession.status == "completed"
            )
        ).filter(
            Subject.user_id == user_id
        )
        
        if start_date:
            query = query.filter(StudySession.start_time >= datetime.combine(start_date, datetime.min.time()))
        
        if end_date:
            query = query.filter(StudySession.start_time <= datetime.combine(end_date, datetime.max.time()))
        
        query = query.group_by(Subject.id).order_by(desc('total_minutes'))
        
        results = query.all()
        
        return [
            SubjectStats(
                subject_id=str(r.id),
                subject_name=r.name,
                subject_color=r.color,
                subject_icon=r.icon,
                total_sessions=r.session_count or 0,
                total_minutes=int(r.total_minutes or 0),
                average_productivity=round(float(r.avg_productivity or 0), 2)
            )
            for r in results
        ]
    
    @staticmethod
    def get_productivity_trends(
        db: Session,
        user_id: UUID,
        days: int = 30
    ) -> List[ProductivityTrend]:
        """Get daily productivity trends"""
        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)
        
        # Query sessions grouped by date
        sessions = db.query(StudySession).filter(
            and_(
                StudySession.user_id == user_id,
                StudySession.status == "completed",
                StudySession.start_time >= datetime.combine(start_date, datetime.min.time())
            )
        ).all()
        
        # Group by date
        daily_data = defaultdict(lambda: {
            'minutes': 0,
            'sessions': 0,
            'productivity_scores': [],
            'focus_scores': []
        })
        
        for session in sessions:
            session_date = session.start_time.date()
            daily_data[session_date]['minutes'] += session.actual_duration_minutes or 0
            daily_data[session_date]['sessions'] += 1
            if session.productivity_score is not None:
                daily_data[session_date]['productivity_scores'].append(session.productivity_score)
            if session.focus_score is not None:
                daily_data[session_date]['focus_scores'].append(session.focus_score)
        
        # Create trend data for all days
        trends = []
        current_date = start_date
        while current_date <= end_date:
            data = daily_data[current_date]
            
            avg_productivity = (
                sum(data['productivity_scores']) / len(data['productivity_scores'])
                if data['productivity_scores'] else 0
            )
            
            avg_focus = (
                sum(data['focus_scores']) / len(data['focus_scores'])
                if data['focus_scores'] else 0
            )
            
            trends.append(ProductivityTrend(
                date=current_date,
                total_minutes=data['minutes'],
                session_count=data['sessions'],
                average_productivity=round(avg_productivity, 2),
                average_focus=round(avg_focus, 2)
            ))
            
            current_date += timedelta(days=1)
        
        return trends
    
    @staticmethod
    def get_goal_progress(
        db: Session,
        user_id: UUID,
        subject_id: Optional[UUID] = None
    ) -> List[GoalProgress]:
        """Get progress for all active goals"""
        query = db.query(Goal).filter(Goal.user_id == user_id)
        
        if subject_id:
            query = query.filter(Goal.subject_id == subject_id)
        
        goals = query.all()
        
        progress_list = []
        for goal in goals:
            # Get subject name
            subject = db.query(Subject).filter(Subject.id == goal.subject_id).first()
            subject_name = subject.name if subject else "Unknown"
            
            # Calculate progress percentage
            progress_percentage = (
                (goal.current_hours / goal.target_hours * 100)
                if goal.target_hours > 0 else 0
            )
            
            # Calculate days remaining
            if goal.end_date:
                days_remaining = (goal.end_date - date.today()).days
            else:
                days_remaining = None
            
            progress_list.append(GoalProgress(
                goal_id=str(goal.id),
                title=f"{goal.goal_type} - {goal.target_hours}h",
                subject_name=subject_name,
                goal_type=goal.goal_type,
                current_value=goal.current_hours,
                target_value=goal.target_hours,
                progress_percentage=round(progress_percentage, 2),
                is_achieved=goal.is_achieved,
                days_remaining=days_remaining,
                target_date=goal.end_date
            ))
        
        return progress_list
    
    @staticmethod
    def get_streak_info(db: Session, user_id: UUID) -> StreakInfo:
        """Get study streak information"""
        streak = db.query(StudyStreak).filter(StudyStreak.user_id == user_id).first()
        
        if not streak:
            return StreakInfo(
                current_streak=0,
                longest_streak=0,
                last_study_date=None,
                total_study_days=0
            )
        
        return StreakInfo(
            current_streak=streak.current_streak,
            longest_streak=streak.longest_streak,
            last_study_date=streak.last_study_date,
            total_study_days=streak.current_streak  # Approximate from current streak
        )
    
    @staticmethod
    def get_wellness_correlation(
        db: Session,
        user_id: UUID,
        days: int = 30
    ) -> WellnessCorrelation:
        """Analyze correlation between wellness metrics and productivity"""
        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)
        
        # Get wellness entries
        wellness_entries = db.query(DailyWellness).filter(
            and_(
                DailyWellness.user_id == user_id,
                DailyWellness.date >= start_date,
                DailyWellness.date <= end_date
            )
        ).all()
        
        # Get sessions for the same period
        sessions = db.query(StudySession).filter(
            and_(
                StudySession.user_id == user_id,
                StudySession.status == "completed",
                StudySession.start_time >= datetime.combine(start_date, datetime.min.time())
            )
        ).all()
        
        # Group sessions by date
        daily_productivity = defaultdict(list)
        for session in sessions:
            if session.productivity_score is not None:
                daily_productivity[session.start_time.date()].append(session.productivity_score)
        
        # Correlate with wellness data
        correlations = []
        for wellness in wellness_entries:
            if wellness.date in daily_productivity:
                avg_productivity = sum(daily_productivity[wellness.date]) / len(daily_productivity[wellness.date])
                
                correlations.append({
                    'sleep_hours': wellness.sleep_hours,
                    'sleep_quality': wellness.sleep_quality,
                    'energy_level': wellness.energy_level,
                    'stress_level': wellness.stress_level,
                    'productivity': avg_productivity
                })
        
        if not correlations:
            return WellnessCorrelation(
                average_sleep_hours=0,
                average_productivity=0,
                high_productivity_sleep_average=0,
                low_productivity_sleep_average=0,
                optimal_sleep_range=(0, 0),
                energy_productivity_correlation="No data available"
            )
        
        # Calculate averages
        avg_sleep = sum(c['sleep_hours'] for c in correlations) / len(correlations)
        avg_productivity = sum(c['productivity'] for c in correlations) / len(correlations)
        
        # Sort by productivity and compare sleep patterns
        sorted_by_productivity = sorted(correlations, key=lambda x: x['productivity'])
        
        # Top 30% and bottom 30%
        top_30_percent = int(len(sorted_by_productivity) * 0.3) or 1
        
        high_productivity_sessions = sorted_by_productivity[-top_30_percent:]
        low_productivity_sessions = sorted_by_productivity[:top_30_percent]
        
        high_prod_sleep = (
            sum(s['sleep_hours'] for s in high_productivity_sessions) / len(high_productivity_sessions)
            if high_productivity_sessions else 0
        )
        
        low_prod_sleep = (
            sum(s['sleep_hours'] for s in low_productivity_sessions) / len(low_productivity_sessions)
            if low_productivity_sessions else 0
        )
        
        # Find optimal sleep range (where productivity is highest)
        sleep_ranges = defaultdict(list)
        for c in correlations:
            sleep_bucket = int(c['sleep_hours'])
            sleep_ranges[sleep_bucket].append(c['productivity'])
        
        if sleep_ranges:
            avg_by_sleep = {
                hours: sum(prods) / len(prods)
                for hours, prods in sleep_ranges.items()
            }
            optimal_sleep = max(avg_by_sleep.items(), key=lambda x: x[1])[0]
            optimal_range = (optimal_sleep, optimal_sleep + 1)
        else:
            optimal_range = (7, 9)
        
        # Energy-productivity correlation
        avg_energy = sum(c['energy_level'] for c in correlations) / len(correlations)
        if avg_energy >= 7 and avg_productivity >= 7:
            energy_correlation = "Strong positive correlation"
        elif avg_energy >= 6 and avg_productivity >= 6:
            energy_correlation = "Moderate positive correlation"
        else:
            energy_correlation = "Need more consistent data"
        
        return WellnessCorrelation(
            average_sleep_hours=round(avg_sleep, 1),
            average_productivity=round(avg_productivity, 1),
            high_productivity_sleep_average=round(high_prod_sleep, 1),
            low_productivity_sleep_average=round(low_prod_sleep, 1),
            optimal_sleep_range=optimal_range,
            energy_productivity_correlation=energy_correlation
        )
    
    @staticmethod
    def get_dashboard_analytics(
        db: Session,
        user_id: UUID,
        days: int = 30
    ) -> DashboardAnalytics:
        """Get comprehensive dashboard analytics"""
        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)
        
        # Get all stats
        study_time_stats = AnalyticsService.get_study_time_stats(
            db, user_id, start_date, end_date
        )
        
        subject_stats = AnalyticsService.get_subject_stats(
            db, user_id, start_date, end_date
        )
        
        productivity_trends = AnalyticsService.get_productivity_trends(
            db, user_id, days
        )
        
        goal_progress = AnalyticsService.get_goal_progress(db, user_id)
        
        streak_info = AnalyticsService.get_streak_info(db, user_id)
        
        wellness_correlation = AnalyticsService.get_wellness_correlation(
            db, user_id, days
        )
        
        # Get upcoming deadlines
        upcoming_deadlines = db.query(Deadline).filter(
            and_(
                Deadline.user_id == user_id,
                Deadline.is_completed == False,
                Deadline.deadline_date >= datetime.now()
            )
        ).order_by(Deadline.deadline_date).limit(5).all()
        
        upcoming_deadlines_list = [
            {
                'id': str(d.id),
                'title': d.title,
                'subject_id': str(d.subject_id),
                'deadline_date': d.deadline_date.isoformat(),
                'priority': d.priority,
                'days_until': (d.deadline_date.date() - date.today()).days
            }
            for d in upcoming_deadlines
        ]
        
        return DashboardAnalytics(
            study_time_stats=study_time_stats,
            subject_stats=subject_stats,
            productivity_trends=productivity_trends,
            goal_progress=goal_progress,
            streak_info=streak_info,
            wellness_correlation=wellness_correlation,
            upcoming_deadlines=upcoming_deadlines_list
        )

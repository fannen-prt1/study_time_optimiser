from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import datetime, timedelta

from app.models.study_session import StudySession
from app.schemas.study_session import (
    StudySessionCreate,
    StudySessionUpdate,
    StudySessionComplete,
    SessionStatus
)


class StudySessionService:
    """Service for managing study sessions"""
    
    @staticmethod
    def create_session(
        db: Session,
        session_data: StudySessionCreate,
        user_id: UUID
    ) -> StudySession:
        """Create a new study session"""
        session = StudySession(
            user_id=user_id,
            subject_id=session_data.subject_id,
            session_type=session_data.session_type.value,
            planned_duration_minutes=session_data.planned_duration_minutes,
            notes=session_data.notes if hasattr(session_data, 'notes') else None,
            status=SessionStatus.ACTIVE.value,
            start_time=session_data.start_time or datetime.utcnow()
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def start_session(db: Session, session_id: UUID, user_id: UUID) -> Optional[StudySession]:
        """Start a study session"""
        session = db.query(StudySession).filter(
            and_(StudySession.id == session_id, StudySession.user_id == user_id)
        ).first()
        
        if not session:
            return None
        
        session.status = SessionStatus.ACTIVE.value
        session.start_time = datetime.utcnow()
        session.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def pause_session(db: Session, session_id: UUID, user_id: UUID) -> Optional[StudySession]:
        """Pause a study session"""
        session = db.query(StudySession).filter(
            and_(StudySession.id == session_id, StudySession.user_id == user_id)
        ).first()
        
        if not session or session.status != SessionStatus.ACTIVE.value:
            return None
        
        session.status = SessionStatus.PAUSED.value
        session.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def resume_session(db: Session, session_id: UUID, user_id: UUID) -> Optional[StudySession]:
        """Resume a paused study session"""
        session = db.query(StudySession).filter(
            and_(StudySession.id == session_id, StudySession.user_id == user_id)
        ).first()
        
        if not session or session.status != SessionStatus.PAUSED.value:
            return None
        
        session.status = SessionStatus.ACTIVE.value
        session.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def complete_session(
        db: Session,
        session_id: UUID,
        user_id: UUID,
        completion_data: StudySessionComplete
    ) -> Optional[StudySession]:
        """Complete a study session"""
        session = db.query(StudySession).filter(
            and_(StudySession.id == session_id, StudySession.user_id == user_id)
        ).first()
        
        if not session:
            return None
        
        session.status = SessionStatus.COMPLETED.value
        session.end_time = datetime.utcnow()
        # Calculate actual duration from start_time
        if session.start_time:
            delta = datetime.utcnow() - session.start_time
            session.actual_duration_minutes = int(delta.total_seconds() / 60)
        session.productivity_score = completion_data.productivity_score
        session.focus_score = completion_data.focus_score
        session.energy_level = completion_data.energy_level
        session.difficulty_level = completion_data.difficulty_level
        session.satisfaction_level = completion_data.satisfaction_level
        if completion_data.notes:
            session.notes = completion_data.notes
        session.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def get_session(db: Session, session_id: UUID, user_id: UUID) -> Optional[StudySession]:
        """Get a specific study session"""
        return db.query(StudySession).filter(
            and_(StudySession.id == session_id, StudySession.user_id == user_id)
        ).first()
    
    @staticmethod
    def get_sessions(
        db: Session,
        user_id: UUID,
        subject_id: Optional[UUID] = None,
        status: Optional[SessionStatus] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[StudySession]:
        """Get study sessions with filters"""
        query = db.query(StudySession).filter(StudySession.user_id == user_id)
        
        if subject_id:
            query = query.filter(StudySession.subject_id == subject_id)
        
        if status:
            query = query.filter(StudySession.status == status.value)
        
        if start_date:
            query = query.filter(StudySession.start_time >= start_date)
        
        if end_date:
            query = query.filter(StudySession.start_time <= end_date)
        
        return query.order_by(desc(StudySession.start_time)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_session(
        db: Session,
        session_id: UUID,
        user_id: UUID,
        session_data: StudySessionUpdate
    ) -> Optional[StudySession]:
        """Update a study session"""
        session = StudySessionService.get_session(db, session_id, user_id)
        if not session:
            return None
        
        update_data = session_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "status" and value:
                setattr(session, field, value.value)
            else:
                setattr(session, field, value)
        
        session.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def delete_session(db: Session, session_id: UUID, user_id: UUID) -> bool:
        """Delete a study session"""
        session = StudySessionService.get_session(db, session_id, user_id)
        if not session:
            return False
        
        db.delete(session)
        db.commit()
        return True

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import datetime

from app.models.deadline import Deadline
from app.schemas.deadline import DeadlineCreate, DeadlineUpdate


class DeadlineService:
    """Service for managing deadlines"""
    
    @staticmethod
    def create_deadline(db: Session, deadline_data: DeadlineCreate, user_id: UUID) -> Deadline:
        """Create a new deadline"""
        deadline = Deadline(
            user_id=user_id,
            subject_id=deadline_data.subject_id,
            title=deadline_data.title,
            description=deadline_data.description,
            deadline_date=deadline_data.deadline_date,
            priority=deadline_data.priority.value,
            is_completed=False,
            reminder_sent=False
        )
        db.add(deadline)
        db.commit()
        db.refresh(deadline)
        return deadline
    
    @staticmethod
    def get_deadline(db: Session, deadline_id: UUID, user_id: UUID) -> Optional[Deadline]:
        """Get a specific deadline"""
        return db.query(Deadline).filter(
            and_(Deadline.id == deadline_id, Deadline.user_id == user_id)
        ).first()
    
    @staticmethod
    def get_deadlines(
        db: Session,
        user_id: UUID,
        subject_id: Optional[UUID] = None,
        is_completed: Optional[bool] = None,
        priority: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Deadline]:
        """Get deadlines with filters"""
        query = db.query(Deadline).filter(Deadline.user_id == user_id)
        
        if subject_id:
            query = query.filter(Deadline.subject_id == subject_id)
        
        if is_completed is not None:
            query = query.filter(Deadline.is_completed == is_completed)
        
        if priority:
            query = query.filter(Deadline.priority == priority)
        
        return query.order_by(Deadline.deadline_date).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_deadline(
        db: Session,
        deadline_id: UUID,
        user_id: UUID,
        deadline_data: DeadlineUpdate
    ) -> Optional[Deadline]:
        """Update a deadline"""
        deadline = DeadlineService.get_deadline(db, deadline_id, user_id)
        if not deadline:
            return None
        
        update_data = deadline_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "priority" and value:
                setattr(deadline, field, value.value)
            else:
                setattr(deadline, field, value)
        
        deadline.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(deadline)
        return deadline
    
    @staticmethod
    def mark_completed(
        db: Session,
        deadline_id: UUID,
        user_id: UUID
    ) -> Optional[Deadline]:
        """Mark a deadline as completed"""
        deadline = DeadlineService.get_deadline(db, deadline_id, user_id)
        if not deadline:
            return None
        
        deadline.is_completed = True
        deadline.completed_at = datetime.utcnow()
        deadline.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(deadline)
        return deadline
    
    @staticmethod
    def mark_incomplete(
        db: Session,
        deadline_id: UUID,
        user_id: UUID
    ) -> Optional[Deadline]:
        """Mark a deadline as incomplete"""
        deadline = DeadlineService.get_deadline(db, deadline_id, user_id)
        if not deadline:
            return None
        
        deadline.is_completed = False
        deadline.completed_at = None
        deadline.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(deadline)
        return deadline
    
    @staticmethod
    def delete_deadline(db: Session, deadline_id: UUID, user_id: UUID) -> bool:
        """Delete a deadline"""
        deadline = DeadlineService.get_deadline(db, deadline_id, user_id)
        if not deadline:
            return False
        
        db.delete(deadline)
        db.commit()
        return True

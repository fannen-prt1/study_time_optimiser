from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime

from app.models.subject import Subject
from app.schemas.subject import SubjectCreate, SubjectUpdate


class SubjectService:
    """Service for managing subjects"""
    
    @staticmethod
    def create_subject(db: Session, subject_data: SubjectCreate, user_id: UUID) -> Subject:
        """Create a new subject for a user"""
        subject = Subject(
            user_id=user_id,
            name=subject_data.name,
            color=subject_data.color,
            icon=subject_data.icon,
            description=subject_data.description
        )
        db.add(subject)
        db.commit()
        db.refresh(subject)
        return subject
    
    @staticmethod
    def get_subject(db: Session, subject_id: UUID, user_id: UUID) -> Optional[Subject]:
        """Get a specific subject by ID for a user"""
        return db.query(Subject).filter(
            and_(Subject.id == subject_id, Subject.user_id == user_id)
        ).first()
    
    @staticmethod
    def get_subjects(
        db: Session,
        user_id: UUID,
        include_archived: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> List[Subject]:
        """Get all subjects for a user"""
        query = db.query(Subject).filter(Subject.user_id == user_id)
        
        if not include_archived:
            query = query.filter(Subject.is_archived == False)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_subject(
        db: Session,
        subject_id: UUID,
        user_id: UUID,
        subject_data: SubjectUpdate
    ) -> Optional[Subject]:
        """Update a subject"""
        subject = SubjectService.get_subject(db, subject_id, user_id)
        if not subject:
            return None
        
        update_data = subject_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(subject, field, value)
        
        subject.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(subject)
        return subject
    
    @staticmethod
    def delete_subject(db: Session, subject_id: UUID, user_id: UUID) -> bool:
        """Delete a subject (hard delete)"""
        subject = SubjectService.get_subject(db, subject_id, user_id)
        if not subject:
            return False
        
        db.delete(subject)
        db.commit()
        return True
    
    @staticmethod
    def archive_subject(db: Session, subject_id: UUID, user_id: UUID) -> Optional[Subject]:
        """Archive a subject (soft delete)"""
        subject = SubjectService.get_subject(db, subject_id, user_id)
        if not subject:
            return None
        
        subject.is_archived = True
        subject.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(subject)
        return subject
    
    @staticmethod
    def unarchive_subject(db: Session, subject_id: UUID, user_id: UUID) -> Optional[Subject]:
        """Unarchive a subject"""
        subject = SubjectService.get_subject(db, subject_id, user_id)
        if not subject:
            return None
        
        subject.is_archived = False
        subject.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(subject)
        return subject

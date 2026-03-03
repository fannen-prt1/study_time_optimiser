from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import datetime, date

from app.models.daily_wellness import DailyWellness
from app.schemas.daily_wellness import DailyWellnessCreate, DailyWellnessUpdate


class WellnessService:
    """Service for managing daily wellness entries"""
    
    @staticmethod
    def create_wellness_entry(
        db: Session,
        wellness_data: DailyWellnessCreate,
        user_id: UUID
    ) -> DailyWellness:
        """Create a new wellness entry"""
        # Check if entry already exists for this date
        existing = db.query(DailyWellness).filter(
            and_(
                DailyWellness.user_id == user_id,
                DailyWellness.date == wellness_data.date
            )
        ).first()
        
        if existing:
            # Update existing entry
            return WellnessService.update_wellness_entry(
                db, existing.id, user_id, 
                DailyWellnessUpdate(**wellness_data.model_dump())
            )
        
        wellness = DailyWellness(
            user_id=user_id,
            date=wellness_data.date,
            sleep_hours=wellness_data.sleep_hours,
            sleep_quality=wellness_data.sleep_quality,
            energy_level=wellness_data.energy_level,
            stress_level=wellness_data.stress_level,
            mood=wellness_data.mood,
            focus_score=wellness_data.focus_score,
            notes=wellness_data.notes
        )
        db.add(wellness)
        db.commit()
        db.refresh(wellness)
        return wellness
    
    @staticmethod
    def get_wellness_entry(
        db: Session,
        wellness_id: UUID,
        user_id: UUID
    ) -> Optional[DailyWellness]:
        """Get a specific wellness entry"""
        return db.query(DailyWellness).filter(
            and_(DailyWellness.id == wellness_id, DailyWellness.user_id == user_id)
        ).first()
    
    @staticmethod
    def get_wellness_by_date(
        db: Session,
        user_id: UUID,
        date: date
    ) -> Optional[DailyWellness]:
        """Get wellness entry for a specific date"""
        return db.query(DailyWellness).filter(
            and_(DailyWellness.user_id == user_id, DailyWellness.date == date)
        ).first()
    
    @staticmethod
    def get_wellness_entries(
        db: Session,
        user_id: UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[DailyWellness]:
        """Get wellness entries with date filters"""
        query = db.query(DailyWellness).filter(DailyWellness.user_id == user_id)
        
        if start_date:
            query = query.filter(DailyWellness.date >= start_date)
        
        if end_date:
            query = query.filter(DailyWellness.date <= end_date)
        
        return query.order_by(desc(DailyWellness.date)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_wellness_entry(
        db: Session,
        wellness_id: UUID,
        user_id: UUID,
        wellness_data: DailyWellnessUpdate
    ) -> Optional[DailyWellness]:
        """Update a wellness entry"""
        wellness = WellnessService.get_wellness_entry(db, wellness_id, user_id)
        if not wellness:
            return None
        
        update_data = wellness_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(wellness, field, value)
        
        wellness.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(wellness)
        return wellness
    
    @staticmethod
    def delete_wellness_entry(db: Session, wellness_id: UUID, user_id: UUID) -> bool:
        """Delete a wellness entry"""
        wellness = WellnessService.get_wellness_entry(db, wellness_id, user_id)
        if not wellness:
            return False
        
        db.delete(wellness)
        db.commit()
        return True

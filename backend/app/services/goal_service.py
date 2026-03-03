from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import datetime, timedelta

from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate


class GoalService:
    """Service for managing goals"""
    
    @staticmethod
    def _compute_end_date(start_date, goal_type: str):
        """Compute end date based on goal type"""
        if goal_type == "daily":
            return start_date + timedelta(days=1)
        elif goal_type == "weekly":
            return start_date + timedelta(weeks=1)
        elif goal_type == "monthly":
            return start_date + timedelta(days=30)
        return start_date + timedelta(weeks=1)
    
    @staticmethod
    def create_goal(db: Session, goal_data: GoalCreate, user_id: UUID) -> Goal:
        """Create a new goal"""
        start = goal_data.start_date
        end = GoalService._compute_end_date(start, goal_data.goal_type.value)
        goal = Goal(
            user_id=user_id,
            subject_id=goal_data.subject_id,
            goal_type=goal_data.goal_type.value,
            target_hours=goal_data.target_hours,
            start_date=start,
            end_date=end,
            current_hours=0,
            is_achieved=False
        )
        db.add(goal)
        db.commit()
        db.refresh(goal)
        return goal
    
    @staticmethod
    def get_goal(db: Session, goal_id: UUID, user_id: UUID) -> Optional[Goal]:
        """Get a specific goal"""
        return db.query(Goal).filter(
            and_(Goal.id == goal_id, Goal.user_id == user_id)
        ).first()
    
    @staticmethod
    def get_goals(
        db: Session,
        user_id: UUID,
        subject_id: Optional[UUID] = None,
        is_achieved: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Goal]:
        """Get goals with filters"""
        query = db.query(Goal).filter(Goal.user_id == user_id)
        
        if subject_id:
            query = query.filter(Goal.subject_id == subject_id)
        
        if is_achieved is not None:
            query = query.filter(Goal.is_achieved == is_achieved)
        
        return query.order_by(Goal.end_date).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_goal(
        db: Session,
        goal_id: UUID,
        user_id: UUID,
        goal_data: GoalUpdate
    ) -> Optional[Goal]:
        """Update a goal"""
        goal = GoalService.get_goal(db, goal_id, user_id)
        if not goal:
            return None
        
        update_data = goal_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "goal_type" and value:
                setattr(goal, field, value.value)
            else:
                setattr(goal, field, value)
        
        goal.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(goal)
        return goal
    
    @staticmethod
    def update_progress(
        db: Session,
        goal_id: UUID,
        user_id: UUID,
        progress: float
    ) -> Optional[Goal]:
        """Update goal progress"""
        goal = GoalService.get_goal(db, goal_id, user_id)
        if not goal:
            return None
        
        goal.current_hours = progress
        
        # Auto-mark as achieved if target reached
        if goal.current_hours >= goal.target_hours and not goal.is_achieved:
            goal.is_achieved = True
            goal.achieved_at = datetime.utcnow()
        
        goal.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(goal)
        return goal
    
    @staticmethod
    def mark_achieved(
        db: Session,
        goal_id: UUID,
        user_id: UUID
    ) -> Optional[Goal]:
        """Manually mark a goal as achieved"""
        goal = GoalService.get_goal(db, goal_id, user_id)
        if not goal:
            return None
        
        goal.is_achieved = True
        goal.achieved_at = datetime.utcnow()
        goal.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(goal)
        return goal
    
    @staticmethod
    def delete_goal(db: Session, goal_id: UUID, user_id: UUID) -> bool:
        """Delete a goal"""
        goal = GoalService.get_goal(db, goal_id, user_id)
        if not goal:
            return False
        
        db.delete(goal)
        db.commit()
        return True

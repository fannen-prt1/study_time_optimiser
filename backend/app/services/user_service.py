from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.user import User
from app.schemas.user import UserUpdate
from app.utils.password import hash_password


class UserService:
    """Service for managing user profile"""
    
    @staticmethod
    def get_user(db: Session, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def update_user(
        db: Session,
        user_id: UUID,
        user_data: UserUpdate
    ) -> Optional[User]:
        """Update user profile"""
        user = UserService.get_user(db, user_id)
        if not user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        # Handle password update separately
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))
        
        for field, value in update_data.items():
            if field == "student_type" and value:
                setattr(user, field, value.value)
            else:
                setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> bool:
        """Delete user account"""
        user = UserService.get_user(db, user_id)
        if not user:
            return False
        
        db.delete(user)
        db.commit()
        return True

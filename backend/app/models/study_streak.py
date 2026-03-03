"""
Study Streak model
"""
from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.connection import Base


class StudyStreak(Base):
    """User study streak tracking"""
    
    __tablename__ = "study_streaks"
    
    # Primary Key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Key
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, unique=True)
    
    # Streak Data
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_study_date = Column(Date, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="study_streak")
    
    def __repr__(self):
        return f"<StudyStreak current={self.current_streak} longest={self.longest_streak}>"

"""
Goal model
"""
from sqlalchemy import Column, String, Integer, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.connection import Base


class Goal(Base):
    """User study goals"""
    
    __tablename__ = "goals"
    
    # Primary Key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(String, ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True)
    
    # Goal Details
    goal_type = Column(String, nullable=False, index=True)  # daily, weekly, monthly
    target_hours = Column(Integer, nullable=False)
    
    # Time Period
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False)
    
    # Progress
    current_hours = Column(Float, default=0.0)
    is_achieved = Column(Boolean, default=False)
    achieved_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="goals")
    subject = relationship("Subject", back_populates="goals")
    
    def __repr__(self):
        return f"<Goal {self.goal_type} - {self.target_hours}h>"

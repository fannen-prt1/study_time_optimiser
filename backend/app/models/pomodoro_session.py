"""
Pomodoro Session model
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.connection import Base


class PomodoroSession(Base):
    """Pomodoro technique sessions"""
    
    __tablename__ = "pomodoro_sessions"
    
    # Primary Key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Key
    study_session_id = Column(String, ForeignKey("study_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Pomodoro Details
    pomodoro_number = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, default=25)
    break_duration_minutes = Column(Integer, default=5)
    completed = Column(Boolean, default=False)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    study_session = relationship("StudySession", back_populates="pomodoro_sessions")
    
    def __repr__(self):
        return f"<PomodoroSession #{self.pomodoro_number}>"

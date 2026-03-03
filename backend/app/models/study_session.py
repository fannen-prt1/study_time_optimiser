"""
Study Session model
"""
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.connection import Base


class StudySession(Base):
    """Study session tracking"""
    
    __tablename__ = "study_sessions"
    
    # Primary Key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(String, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Session Details
    session_type = Column(String, nullable=False)  # focused_study, practice, reading, review
    status = Column(String, default="active", index=True)  # active, paused, completed, cancelled
    
    # Time Tracking
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=True)
    planned_duration_minutes = Column(Integer, nullable=True)
    actual_duration_minutes = Column(Integer, nullable=True)
    pause_count = Column(Integer, default=0)
    total_pause_duration_minutes = Column(Integer, default=0)
    
    # Performance Metrics
    productivity_score = Column(Integer, nullable=True)  # 0-100
    focus_score = Column(Integer, nullable=True)  # 0-100
    
    # Feedback
    energy_level = Column(Integer, nullable=True)  # 1-5
    difficulty_level = Column(Integer, nullable=True)  # 1-5
    satisfaction_level = Column(Integer, nullable=True)  # 1-5
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="study_sessions")
    subject = relationship("Subject", back_populates="study_sessions")
    pomodoro_sessions = relationship("PomodoroSession", back_populates="study_session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<StudySession {self.id} - {self.session_type}>"

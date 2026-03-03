"""
Subject model
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.connection import Base


class Subject(Base):
    """Subject/course that user studies"""
    
    __tablename__ = "subjects"
    
    # Primary Key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Key
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Subject Info
    name = Column(String, nullable=False)
    color = Column(String, default="#0ea5e9")
    icon = Column(String, default="📚")
    description = Column(Text, nullable=True)
    is_archived = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subjects")
    study_sessions = relationship("StudySession", back_populates="subject", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="subject")
    deadlines = relationship("Deadline", back_populates="subject", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Subject {self.name}>"

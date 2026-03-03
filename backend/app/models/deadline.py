"""
Deadline model
"""
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.connection import Base


class Deadline(Base):
    """Assignment/exam deadlines"""
    
    __tablename__ = "deadlines"
    
    # Primary Key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Keys
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id = Column(String, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    
    # Deadline Details
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    deadline_date = Column(DateTime, nullable=False, index=True)
    
    # Priority
    priority = Column(String, default="medium", index=True)  # low, medium, high, urgent
    
    # Status
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Notifications
    reminder_sent = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="deadlines")
    subject = relationship("Subject", back_populates="deadlines")
    
    def __repr__(self):
        return f"<Deadline {self.title}>"

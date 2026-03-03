"""
Achievement model
"""
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.connection import Base


class Achievement(Base):
    """User achievements and badges"""
    
    __tablename__ = "achievements"
    
    # Primary Key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Key
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Achievement Details
    badge_type = Column(String, nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow, index=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    
    # Unique constraint
    __table_args__ = (UniqueConstraint('user_id', 'badge_type', name='_user_badge_uc'),)
    
    def __repr__(self):
        return f"<Achievement {self.badge_type}>"

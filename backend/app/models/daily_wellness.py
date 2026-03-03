"""
Daily Wellness model
"""
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.connection import Base


class DailyWellness(Base):
    """Daily wellness and sleep tracking"""
    
    __tablename__ = "daily_wellness"
    
    # Primary Key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Key
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Date
    date = Column(Date, nullable=False, index=True)
    
    # Wellness Metrics
    sleep_hours = Column(Float, nullable=True)  # 0-24
    sleep_quality = Column(Integer, nullable=True)  # 1-5
    energy_level = Column(Integer, nullable=True)  # 1-5
    stress_level = Column(Integer, nullable=True)  # 1-10
    mood = Column(Integer, nullable=True)  # 1-5
    focus_score = Column(Integer, nullable=True)  # 1-100
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships  
    user = relationship("User", back_populates="wellness_entries")
    
    # Unique constraint - one entry per user per day
    __table_args__ = (UniqueConstraint('user_id', 'date', name='_user_date_uc'),)
    
    def __repr__(self):
        return f"<DailyWellness {self.date} - {self.sleep_hours}h sleep>"

"""
AI Prediction model
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship  
from datetime import datetime
import uuid

from app.database.connection import Base


class AIPrediction(Base):
    """AI model predictions"""
    
    __tablename__ = "ai_predictions"
    
    # Primary Key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign Key
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Prediction Type
    prediction_type = Column(String, nullable=False, index=True)  # productivity, optimal_time, duration
    
    # Input Parameters
    subject_id = Column(String, nullable=True)
    time_slot = Column(Integer, nullable=True)
    
    # Prediction Results
    predicted_value = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=True)
    
    # Model Metadata
    model_version = Column(String, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="ai_predictions")
    
    def __repr__(self):
        return f"<AIPrediction {self.prediction_type}>"

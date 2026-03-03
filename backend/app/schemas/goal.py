"""
Goal Pydantic schemas
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
from enum import Enum


class GoalType(str, Enum):
    """Goal type enumeration"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class GoalBase(BaseModel):
    """Base goal schema"""
    goal_type: GoalType
    target_hours: int = Field(..., ge=1, le=168)  # Max weekly hours
    subject_id: Optional[str] = None


class GoalCreate(GoalBase):
    """Schema for creating a goal"""
    start_date: Optional[date] = None  # Defaults to today if not provided
    
    @field_validator('start_date')
    @classmethod
    def set_default_start_date(cls, v):
        """Set default start date to today if not provided"""
        return v or date.today()


class GoalUpdate(BaseModel):
    """Schema for updating a goal"""
    target_hours: Optional[int] = Field(None, ge=1, le=168)
    current_hours: Optional[float] = Field(None, ge=0)


class GoalResponse(GoalBase):
    """Schema for goal in responses"""
    id: str
    user_id: str
    start_date: date
    end_date: date
    current_hours: float
    is_achieved: bool
    achieved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    # Computed field
    @property
    def progress_percentage(self) -> float:
        """Calculate progress percentage"""
        return min((self.current_hours / self.target_hours) * 100, 100.0)
    
    model_config = {
        "from_attributes": True
    }

"""
Deadline Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class PriorityLevel(str, Enum):
    """Priority level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class DeadlineBase(BaseModel):
    """Base deadline schema"""
    subject_id: str
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    deadline_date: datetime
    priority: PriorityLevel = PriorityLevel.MEDIUM


class DeadlineCreate(DeadlineBase):
    """Schema for creating a deadline"""
    pass


class DeadlineUpdate(BaseModel):
    """Schema for updating a deadline"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    deadline_date: Optional[datetime] = None
    priority: Optional[PriorityLevel] = None
    is_completed: Optional[bool] = None


class DeadlineResponse(DeadlineBase):
    """Schema for deadline in responses"""
    id: str
    user_id: str
    is_completed: bool
    completed_at: Optional[datetime] = None
    reminder_sent: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }

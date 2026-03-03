"""
Study Session Pydantic schemas
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class SessionType(str, Enum):
    """Study session type"""
    FOCUSED_STUDY = "focused_study"
    PRACTICE = "practice"
    READING = "reading"
    REVIEW = "review"


class SessionStatus(str, Enum):
    """Study session status"""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class StudySessionBase(BaseModel):
    """Base study session schema"""
    subject_id: str
    session_type: SessionType
    planned_duration_minutes: Optional[int] = Field(None, ge=1, le=480)  # Max 8 hours


class StudySessionCreate(StudySessionBase):
    """Schema for creating a study session"""
    start_time: Optional[datetime] = None  # Defaults to now if not provided
    notes: Optional[str] = Field(None, max_length=1000)


class StudySessionUpdate(BaseModel):
    """Schema for updating a study session"""
    session_type: Optional[SessionType] = None
    status: Optional[SessionStatus] = None
    end_time: Optional[datetime] = None
    actual_duration_minutes: Optional[int] = Field(None, ge=0)
    productivity_score: Optional[int] = Field(None, ge=0, le=100)
    focus_score: Optional[int] = Field(None, ge=0, le=100)
    energy_level: Optional[int] = Field(None, ge=1, le=5)
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    satisfaction_level: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = Field(None, max_length=1000)


class StudySessionComplete(BaseModel):
    """Schema for completing a study session"""
    productivity_score: Optional[int] = Field(None, ge=0, le=100)
    focus_score: Optional[int] = Field(None, ge=0, le=100)
    energy_level: Optional[int] = Field(None, ge=1, le=5)
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    satisfaction_level: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = Field(None, max_length=1000)


class StudySessionResponse(StudySessionBase):
    """Schema for study session in responses"""
    id: str
    user_id: str
    status: SessionStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    actual_duration_minutes: Optional[int] = None
    pause_count: int
    total_pause_duration_minutes: int
    productivity_score: Optional[int] = None
    focus_score: Optional[int] = None
    energy_level: Optional[int] = None
    difficulty_level: Optional[int] = None
    satisfaction_level: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }

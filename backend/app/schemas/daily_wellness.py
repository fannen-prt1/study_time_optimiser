"""
Daily Wellness Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class DailyWellnessBase(BaseModel):
    """Base daily wellness schema"""
    date: date
    sleep_hours: Optional[float] = Field(None, ge=0, le=24)
    sleep_quality: Optional[int] = Field(None, ge=1, le=5)
    energy_level: Optional[int] = Field(None, ge=1, le=5)
    stress_level: Optional[int] = Field(None, ge=1, le=10)
    mood: Optional[int] = Field(None, ge=1, le=5)
    focus_score: Optional[int] = Field(None, ge=1, le=100)
    notes: Optional[str] = Field(None, max_length=500)


class DailyWellnessCreate(DailyWellnessBase):
    """Schema for creating a wellness entry"""
    pass


class DailyWellnessUpdate(BaseModel):
    """Schema for updating a wellness entry"""
    sleep_hours: Optional[float] = Field(None, ge=0, le=24)
    sleep_quality: Optional[int] = Field(None, ge=1, le=5)
    energy_level: Optional[int] = Field(None, ge=1, le=5)
    stress_level: Optional[int] = Field(None, ge=1, le=10)
    mood: Optional[int] = Field(None, ge=1, le=5)
    focus_score: Optional[int] = Field(None, ge=1, le=100)
    notes: Optional[str] = Field(None, max_length=500)


class DailyWellnessResponse(DailyWellnessBase):
    """Schema for wellness entry in responses"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }

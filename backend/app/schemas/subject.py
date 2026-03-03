"""
Subject Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SubjectBase(BaseModel):
    """Base subject schema"""
    name: str = Field(..., min_length=1, max_length=100)
    color: str = Field(default="#0ea5e9", pattern=r'^#[0-9A-Fa-f]{6}$')
    icon: str = Field(default="📚", max_length=10)
    description: Optional[str] = Field(None, max_length=500)


class SubjectCreate(SubjectBase):
    """Schema for creating a subject"""
    pass


class SubjectUpdate(BaseModel):
    """Schema for updating a subject"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    icon: Optional[str] = Field(None, max_length=10)
    description: Optional[str] = Field(None, max_length=500)
    is_archived: Optional[bool] = None


class SubjectResponse(SubjectBase):
    """Schema for subject in responses"""
    id: str
    user_id: str
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }

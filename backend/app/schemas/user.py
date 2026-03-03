"""
User Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class StudentType(str, Enum):
    """Student type enumeration"""
    HIGH_SCHOOL = "high_school"
    COLLEGE = "college"
    GRADUATE = "graduate"
    PROFESSIONAL = "professional"


# Base schema with common fields
class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=13, le=120)
    student_type: StudentType


# Schema for creating a new user
class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


# Schema for updating user
class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=13, le=120)
    student_type: Optional[StudentType] = None
    profile_image_url: Optional[str] = None


# Schema for password change
class PasswordChange(BaseModel):
    """Schema for changing password"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


# Schema for password reset request
class PasswordResetRequest(BaseModel):
    """Schema for requesting password reset"""
    email: EmailStr


# Schema for password reset
class PasswordReset(BaseModel):
    """Schema for resetting password"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


# Schema for user response
class UserResponse(UserBase):
    """Schema for user data in responses"""
    id: str
    profile_image_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }


# Schema for user in database (includes sensitive fields)
class UserInDB(UserResponse):
    """Schema for user data stored in database"""
    password_hash: str

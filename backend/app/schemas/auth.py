"""
Authentication Pydantic schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    """Schema for login request"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenRefreshRequest(BaseModel):
    """Schema for refreshing access token"""
    refresh_token: str


class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[str] = None
    email: Optional[str] = None


class EmailVerificationRequest(BaseModel):
    """Schema for email verification with 6-digit code"""
    email: EmailStr
    code: str


class ResendVerificationRequest(BaseModel):
    """Schema for resending verification code"""
    email: EmailStr

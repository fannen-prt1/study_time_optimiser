"""
Authentication service with all auth-related business logic
"""
from datetime import datetime, timedelta
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.models.study_streak import StudyStreak
from app.schemas.user import UserCreate
from app.schemas.auth import TokenResponse
from app.utils.password import hash_password, verify_password
from app.utils.jwt import (
    create_access_token, create_refresh_token,
    generate_verification_code, generate_reset_token, decode_token
)
from app.utils.email import (
    send_verification_email, send_password_reset_email, send_welcome_email
)
from app.config.settings import settings

# Verification code is valid for 5 minutes
VERIFICATION_CODE_EXPIRY_MINUTES = 5


class AuthService:
    """Authentication service"""
    
    @staticmethod
    async def register_user(user_data: UserCreate, db: Session) -> User:
        """
        Register a new user
        """
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Generate 6-digit verification code
        verification_code = generate_verification_code()
        code_expires = datetime.utcnow() + timedelta(minutes=VERIFICATION_CODE_EXPIRY_MINUTES)
        
        # Create user
        user = User(
            email=user_data.email,
            password_hash=hashed_password,
            full_name=user_data.full_name,
            age=user_data.age,
            student_type=user_data.student_type.value,
            verification_code=verification_code,
            verification_code_expires=code_expires,
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create study streak for user
        streak = StudyStreak(user_id=user.id)
        db.add(streak)
        db.commit()
        
        # Send verification email with 6-digit code
        await send_verification_email(user.email, verification_code, user.full_name)
        
        return user
    
    @staticmethod
    async def login(email: str, password: str, db: Session) -> TokenResponse:
        """
        Authenticate user and generate tokens.
        Blocks login for unverified accounts.
        """
        # Get user
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Block login for unverified users
        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email not verified. Please check your email for the verification code."
            )
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Generate tokens
        access_token = create_access_token(data={"sub": user.id, "email": user.email})
        refresh_token_str = create_refresh_token(data={"sub": user.id})
        
        # Store refresh token in database
        refresh_token = RefreshToken(
            user_id=user.id,
            token=refresh_token_str,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(refresh_token)
        db.commit()
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token_str,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    @staticmethod
    async def refresh_access_token(refresh_token_str: str, db: Session) -> TokenResponse:
        """
        Refresh access token using refresh token
        
        Args:
            refresh_token_str: Refresh token
            db: Database  session
            
        Returns:
            New access and refresh tokens
            
        Raises:
            HTTPException: If refresh token is invalid
        """
        # Decode token
        try:
            payload = decode_token(refresh_token_str)
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type"
                )
            user_id = payload.get("sub")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Check if token exists and is valid
        refresh_token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token_str,
            RefreshToken.user_id == user_id
        ).first()
        
        if not refresh_token or refresh_token.is_revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or revoked refresh token"
            )
        
        if refresh_token.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )
        
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Revoke old refresh token
        refresh_token.is_revoked = True
        
        # Generate new tokens
        access_token = create_access_token(data={"sub": user.id, "email": user.email})
        new_refresh_token_str = create_refresh_token(data={"sub": user.id})
        
        # Store new refresh token
        new_refresh_token = RefreshToken(
            user_id=user.id,
            token=new_refresh_token_str,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(new_refresh_token)
        db.commit()
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token_str,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    @staticmethod
    async def verify_email(email: str, code: str, db: Session) -> bool:
        """
        Verify user email with 6-digit code
        """
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No account found with this email"
            )
        
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified"
            )
        
        if not user.verification_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No verification code found. Please request a new one."
            )
        
        # Check if code has expired
        if user.verification_code_expires and user.verification_code_expires < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification code has expired. Please request a new one."
            )
        
        # Check if code matches
        if user.verification_code != code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid verification code"
            )
        
        # Verify user
        user.is_verified = True
        user.verification_code = None
        user.verification_code_expires = None
        db.commit()
        
        # Send welcome email
        await send_welcome_email(user.email, user.full_name)
        
        return True
    
    @staticmethod
    async def request_password_reset(email: str, db: Session) -> bool:
        """
        Request password reset
        
        Args:
            email: User email
            db: Database session
            
        Returns:
            True if request processed
        """
        user = db.query(User).filter(User.email == email).first()
        
        # Don't reveal if email exists or not (security best practice)
        if not user:
            return True
        
        # Generate reset token
        reset_token = generate_reset_token()
        
        # Set token and expiration (1 hour)
        user.reset_password_token = reset_token
        user.reset_password_expires = datetime.utcnow() + timedelta(hours=1)
        db.commit()
        
        # Send reset email
        await send_password_reset_email(user.email, reset_token)
        
        return True
    
    @staticmethod
    async def reset_password(token: str, new_password: str, db: Session) -> bool:
        """
        Reset password with token
        
        Args:
            token: Reset token
            new_password: New password
            db: Database session
            
        Returns:
            True if reset successfully
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        user = db.query(User).filter(User.reset_password_token == token).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid reset token"
            )
        
        if user.reset_password_expires < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token expired"
            )
        
        # Update password
        user.password_hash = hash_password(new_password)
        user.reset_password_token = None
        user.reset_password_expires = None
        
        # Revoke all refresh tokens for security
        db.query(RefreshToken).filter(RefreshToken.user_id == user.id).update(
            {"is_revoked": True}
        )
        
        db.commit()
        
        return True
    
    @staticmethod
    async def resend_verification(email: str, db: Session) -> bool:
        """
        Resend verification code to user.
        """
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Don't reveal if email exists
            return True
        
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified"
            )
        
        # Generate new 6-digit verification code
        new_code = generate_verification_code()
        user.verification_code = new_code
        user.verification_code_expires = datetime.utcnow() + timedelta(minutes=VERIFICATION_CODE_EXPIRY_MINUTES)
        db.commit()
        
        await send_verification_email(user.email, new_code, user.full_name)
        return True

    @staticmethod
    async def logout(refresh_token_str: str, db: Session) -> bool:
        """
        Logout user by revoking refresh token
        
        Args:
            refresh_token_str: Refresh token to revoke
            db: Database session
            
        Returns:
            True if logged out successfully
        """
        refresh_token = db.query(RefreshToken).filter(
            RefreshToken.token == refresh_token_str
        ).first()
        
        if refresh_token:
            refresh_token.is_revoked = True
            db.commit()
        
        return True

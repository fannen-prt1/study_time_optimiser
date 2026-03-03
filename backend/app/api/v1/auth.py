"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.auth_dependencies import get_current_user, get_current_verified_user
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserResponse, PasswordChange, PasswordResetRequest, PasswordReset
from app.schemas.auth import LoginRequest, TokenResponse, TokenRefreshRequest, EmailVerificationRequest, ResendVerificationRequest
from app.models.user import User
from app.utils.password import hash_password, verify_password
from app.config.settings import settings

router = APIRouter()
auth_service = AuthService()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    A 6-digit verification code will be sent to the user's email (or printed to backend console in dev mode).
    """
    user = await auth_service.register_user(user_data, db)
    
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "age": user.age,
        "student_type": user.student_type,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "created_at": str(user.created_at),
        "message": "Account created! Please check your email (or backend console) for the 6-digit verification code.",
    }


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with email and password
    
    Returns access token and refresh token for authenticated requests.
    """
    return await auth_service.login(login_data.email, login_data.password, db)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: TokenRefreshRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    
    When access token expires, use this endpoint to get a new one.
    """
    return await auth_service.refresh_access_token(refresh_data.refresh_token, db)


@router.post("/logout")
async def logout(
    refresh_data: TokenRefreshRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Logout user by revoking refresh token
    """
    await auth_service.logout(refresh_data.refresh_token, db)
    return {"message": "Successfully logged out"}


@router.post("/verify-email")
async def verify_email(
    verification_data: EmailVerificationRequest,
    db: Session = Depends(get_db)
):
    """
    Verify email address with 6-digit code sent to user's email.
    """
    await auth_service.verify_email(verification_data.email, verification_data.code, db)
    return {"message": "Email verified successfully"}


@router.post("/request-password-reset")
async def request_password_reset(
    reset_request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """
    Request password reset email
    
    Sends password reset link to user's email if account exists.
    """
    await auth_service.request_password_reset(reset_request.email, db)
    return {"message": "If email exists, password reset link has been sent"}


@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    """
    Reset password using reset token
    
    Token is received via email from request-password-reset endpoint.
    """
    await auth_service.reset_password(reset_data.token, reset_data.new_password, db)
    return {"message": "Password reset successfully"}


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change password for authenticated user
    
    Requires current password for security.
    """
    # Verify current password
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.password_hash = hash_password(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user's information
    """
    return current_user


@router.get("/me/verified", response_model=UserResponse)
async def get_current_verified_user_info(
    current_user: User = Depends(get_current_verified_user)
):
    """
    Get current verified user's information
    
    Requires email verification.
    """
    return current_user


@router.post("/resend-verification")
async def resend_verification(
    data: ResendVerificationRequest,
    db: Session = Depends(get_db)
):
    """
    Resend verification code to the given email address.
    Does not require authentication.
    """
    await auth_service.resend_verification(data.email, db)
    return {"message": "If the email exists, a new verification code has been sent."}

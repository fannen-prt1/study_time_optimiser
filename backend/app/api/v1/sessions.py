from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.dependencies import get_db
from app.services.auth_dependencies import get_current_verified_user
from app.services.study_session_service import StudySessionService
from app.schemas.study_session import (
    StudySessionCreate,
    StudySessionUpdate,
    StudySessionComplete,
    StudySessionResponse,
    SessionStatus
)
from app.models.user import User

router = APIRouter(prefix="/sessions", tags=["study-sessions"])


@router.post("/", response_model=StudySessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    session_data: StudySessionCreate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Create a new study session"""
    session = StudySessionService.create_session(db, session_data, current_user.id)
    return session


@router.get("/", response_model=List[StudySessionResponse])
def get_sessions(
    subject_id: Optional[str] = Query(None),
    status: Optional[SessionStatus] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get study sessions with filters"""
    sessions = StudySessionService.get_sessions(
        db, current_user.id, subject_id, status, start_date, end_date, skip, limit
    )
    return sessions


@router.get("/{session_id}", response_model=StudySessionResponse)
def get_session(
    session_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get a specific study session"""
    session = StudySessionService.get_session(db, session_id, current_user.id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session


@router.put("/{session_id}", response_model=StudySessionResponse)
def update_session(
    session_id: str,
    session_data: StudySessionUpdate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Update a study session"""
    session = StudySessionService.update_session(db, session_id, current_user.id, session_data)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Delete a study session"""
    success = StudySessionService.delete_session(db, session_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return None


@router.post("/{session_id}/start", response_model=StudySessionResponse)
def start_session(
    session_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Start a study session"""
    session = StudySessionService.start_session(db, session_id, current_user.id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session


@router.post("/{session_id}/pause", response_model=StudySessionResponse)
def pause_session(
    session_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Pause a study session"""
    session = StudySessionService.pause_session(db, session_id, current_user.id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or not in progress"
        )
    return session


@router.post("/{session_id}/resume", response_model=StudySessionResponse)
def resume_session(
    session_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Resume a paused study session"""
    session = StudySessionService.resume_session(db, session_id, current_user.id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or not paused"
        )
    return session


@router.post("/{session_id}/complete", response_model=StudySessionResponse)
def complete_session(
    session_id: str,
    completion_data: StudySessionComplete,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Complete a study session"""
    session = StudySessionService.complete_session(
        db, session_id, current_user.id, completion_data
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session

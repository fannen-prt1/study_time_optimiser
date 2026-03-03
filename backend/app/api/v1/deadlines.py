from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.auth_dependencies import get_current_verified_user
from app.services.deadline_service import DeadlineService
from app.schemas.deadline import DeadlineCreate, DeadlineUpdate, DeadlineResponse
from app.models.user import User

router = APIRouter(prefix="/deadlines", tags=["deadlines"])


@router.post("/", response_model=DeadlineResponse, status_code=status.HTTP_201_CREATED)
def create_deadline(
    deadline_data: DeadlineCreate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Create a new deadline"""
    deadline = DeadlineService.create_deadline(db, deadline_data, current_user.id)
    return deadline


@router.get("/", response_model=List[DeadlineResponse])
def get_deadlines(
    subject_id: Optional[str] = Query(None),
    is_completed: Optional[bool] = Query(None),
    priority: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get deadlines with filters"""
    deadlines = DeadlineService.get_deadlines(
        db, current_user.id, subject_id, is_completed, priority, skip, limit
    )
    return deadlines


@router.get("/{deadline_id}", response_model=DeadlineResponse)
def get_deadline(
    deadline_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get a specific deadline"""
    deadline = DeadlineService.get_deadline(db, deadline_id, current_user.id)
    if not deadline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deadline not found"
        )
    return deadline


@router.put("/{deadline_id}", response_model=DeadlineResponse)
def update_deadline(
    deadline_id: str,
    deadline_data: DeadlineUpdate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Update a deadline"""
    deadline = DeadlineService.update_deadline(db, deadline_id, current_user.id, deadline_data)
    if not deadline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deadline not found"
        )
    return deadline


@router.delete("/{deadline_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deadline(
    deadline_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Delete a deadline"""
    success = DeadlineService.delete_deadline(db, deadline_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deadline not found"
        )
    return None


@router.post("/{deadline_id}/complete", response_model=DeadlineResponse)
def mark_deadline_complete(
    deadline_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Mark a deadline as completed"""
    deadline = DeadlineService.mark_completed(db, deadline_id, current_user.id)
    if not deadline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deadline not found"
        )
    return deadline


@router.post("/{deadline_id}/incomplete", response_model=DeadlineResponse)
def mark_deadline_incomplete(
    deadline_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Mark a deadline as incomplete"""
    deadline = DeadlineService.mark_incomplete(db, deadline_id, current_user.id)
    if not deadline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deadline not found"
        )
    return deadline

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.auth_dependencies import get_current_verified_user
from app.services.subject_service import SubjectService
from app.schemas.subject import SubjectCreate, SubjectUpdate, SubjectResponse
from app.models.user import User

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(
    subject_data: SubjectCreate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Create a new subject"""
    subject = SubjectService.create_subject(db, subject_data, current_user.id)
    return subject


@router.get("/", response_model=List[SubjectResponse])
def get_subjects(
    include_archived: bool = Query(False, description="Include archived subjects"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get all subjects for the current user"""
    subjects = SubjectService.get_subjects(
        db, current_user.id, include_archived, skip, limit
    )
    return subjects


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(
    subject_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get a specific subject"""
    subject = SubjectService.get_subject(db, subject_id, current_user.id)
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    return subject


@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: str,
    subject_data: SubjectUpdate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Update a subject"""
    subject = SubjectService.update_subject(db, subject_id, current_user.id, subject_data)
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    return subject


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(
    subject_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Delete a subject"""
    success = SubjectService.delete_subject(db, subject_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    return None


@router.post("/{subject_id}/archive", response_model=SubjectResponse)
def archive_subject(
    subject_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Archive a subject"""
    subject = SubjectService.archive_subject(db, subject_id, current_user.id)
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    return subject


@router.post("/{subject_id}/unarchive", response_model=SubjectResponse)
def unarchive_subject(
    subject_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Unarchive a subject"""
    subject = SubjectService.unarchive_subject(db, subject_id, current_user.id)
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    return subject

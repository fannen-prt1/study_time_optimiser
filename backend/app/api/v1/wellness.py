from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date

from app.database.dependencies import get_db
from app.services.auth_dependencies import get_current_verified_user
from app.services.wellness_service import WellnessService
from app.schemas.daily_wellness import (
    DailyWellnessCreate,
    DailyWellnessUpdate,
    DailyWellnessResponse
)
from app.models.user import User

router = APIRouter(prefix="/wellness", tags=["wellness"])


@router.post("/", response_model=DailyWellnessResponse, status_code=status.HTTP_201_CREATED)
def log_wellness(
    wellness_data: DailyWellnessCreate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Log daily wellness data"""
    wellness = WellnessService.create_wellness_entry(db, wellness_data, current_user.id)
    return wellness


@router.get("/", response_model=List[DailyWellnessResponse])
def get_wellness_entries(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get wellness entries with date filters"""
    entries = WellnessService.get_wellness_entries(
        db, current_user.id, start_date, end_date, skip, limit
    )
    return entries


@router.get("/date/{wellness_date}", response_model=DailyWellnessResponse)
def get_wellness_by_date(
    wellness_date: date,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get wellness entry for a specific date"""
    wellness = WellnessService.get_wellness_by_date(db, current_user.id, wellness_date)
    if not wellness:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No wellness entry found for this date"
        )
    return wellness


@router.get("/{wellness_id}", response_model=DailyWellnessResponse)
def get_wellness_entry(
    wellness_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get a specific wellness entry"""
    wellness = WellnessService.get_wellness_entry(db, wellness_id, current_user.id)
    if not wellness:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wellness entry not found"
        )
    return wellness


@router.put("/{wellness_id}", response_model=DailyWellnessResponse)
def update_wellness_entry(
    wellness_id: str,
    wellness_data: DailyWellnessUpdate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Update a wellness entry"""
    wellness = WellnessService.update_wellness_entry(db, wellness_id, current_user.id, wellness_data)
    if not wellness:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wellness entry not found"
        )
    return wellness


@router.delete("/{wellness_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wellness_entry(
    wellness_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Delete a wellness entry"""
    success = WellnessService.delete_wellness_entry(db, wellness_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wellness entry not found"
        )
    return None

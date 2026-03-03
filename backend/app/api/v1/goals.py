from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.auth_dependencies import get_current_verified_user
from app.services.goal_service import GoalService
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from app.models.user import User

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(
    goal_data: GoalCreate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Create a new goal"""
    goal = GoalService.create_goal(db, goal_data, current_user.id)
    return goal


@router.get("/", response_model=List[GoalResponse])
def get_goals(
    subject_id: Optional[str] = Query(None),
    is_achieved: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get goals with filters"""
    goals = GoalService.get_goals(db, current_user.id, subject_id, is_achieved, skip, limit)
    return goals


@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(
    goal_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Get a specific goal"""
    goal = GoalService.get_goal(db, goal_id, current_user.id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    return goal


@router.put("/{goal_id}", response_model=GoalResponse)
def update_goal(
    goal_id: str,
    goal_data: GoalUpdate,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Update a goal"""
    goal = GoalService.update_goal(db, goal_id, current_user.id, goal_data)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    return goal


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(
    goal_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Delete a goal"""
    success = GoalService.delete_goal(db, goal_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    return None


@router.post("/{goal_id}/progress", response_model=GoalResponse)
def update_goal_progress(
    goal_id: str,
    progress: float = Body(..., embed=True, ge=0),
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Update goal progress"""
    goal = GoalService.update_progress(db, goal_id, current_user.id, progress)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    return goal


@router.post("/{goal_id}/achieve", response_model=GoalResponse)
def mark_goal_achieved(
    goal_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: Session = Depends(get_db)
):
    """Mark a goal as achieved"""
    goal = GoalService.mark_achieved(db, goal_id, current_user.id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found"
        )
    return goal

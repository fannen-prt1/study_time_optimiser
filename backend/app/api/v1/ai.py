"""
AI endpoints: productivity prediction & peak study hours
"""

import sys
from pathlib import Path
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.auth_dependencies import get_current_user
from app.models.user import User
from app.models.study_session import StudySession
from app.schemas.ai import (
    AiPredictionInput,
    AiProductivityPrediction,
    PeakStudyHoursResponse,
    PeakStudyHour,
)

router = APIRouter(prefix="/ai", tags=["AI"])

# --- Productivity Predictor (loaded once) ---
_predictor = None


def _get_predictor():
    """Lazy-load the trained ML model."""
    global _predictor
    if _predictor is not None:
        return _predictor

    try:
        # Add ml-engine to path so we can import
        # Path: backend/app/api/v1/ai.py -> go up 4 levels to backend/ -> ml-engine/
        ml_engine_dir = Path(__file__).resolve().parent.parent.parent.parent / "ml-engine"
        if str(ml_engine_dir) not in sys.path:
            sys.path.insert(0, str(ml_engine_dir))

        print(f"[AI] Loading ML model from: {ml_engine_dir}")

        from models.productivity_predictor import ProductivityPredictor

        _predictor = ProductivityPredictor()
        if not _predictor.load():
            print("[AI ERROR] Failed to load model file - file may not exist or is corrupted")
            return None

        print("[AI] Model loaded successfully")
        return _predictor
    except Exception as e:
        print(f"[AI ERROR] Exception loading model: {e}")
        import traceback
        traceback.print_exc()
        return None


# --- Endpoints ---


@router.post("/predict-productivity", response_model=AiProductivityPrediction)
async def predict_productivity(
    data: AiPredictionInput,
    current_user: User = Depends(get_current_user),
):
    """Predict productivity score based on current habits."""
    predictor = _get_predictor()
    if predictor is None:
        raise HTTPException(
            status_code=503,
            detail="AI model not available. Please train the model first.",
        )

    try:
        result = predictor.predict(
            study_hours_per_day=data.study_hours_per_day,
            sleep_hours=data.sleep_hours,
            stress_level=data.stress_level,
            focus_score=data.focus_score,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.get("/peak-hours", response_model=PeakStudyHoursResponse)
async def get_peak_hours(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get user's peak study hours from their session history."""
    sessions = (
        db.query(StudySession)
        .filter(
            StudySession.user_id == current_user.id,
            StudySession.status == "completed",
            StudySession.productivity_score.isnot(None),
            StudySession.start_time.isnot(None),
        )
        .all()
    )

    if len(sessions) < 3:
        raise HTTPException(
            status_code=404,
            detail="Not enough completed sessions with productivity scores. Complete at least 3 sessions.",
        )

    # Group by hour of day
    hour_data: dict[int, list[int]] = defaultdict(list)
    for s in sessions:
        hour = s.start_time.hour
        hour_data[hour].append(s.productivity_score)

    peak_hours = []
    for hour, scores in sorted(hour_data.items()):
        peak_hours.append(
            PeakStudyHour(
                hour=hour,
                average_productivity=round(sum(scores) / len(scores), 1),
                session_count=len(scores),
            )
        )

    if not peak_hours:
        raise HTTPException(status_code=404, detail="No session data to analyze.")

    best = max(peak_hours, key=lambda h: h.average_productivity)

    return PeakStudyHoursResponse(
        peak_hours=peak_hours,
        best_hour=best.hour,
        best_productivity=best.average_productivity,
        total_sessions_analyzed=len(sessions),
    )

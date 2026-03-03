"""
AI Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import Optional


class AiPredictionInput(BaseModel):
    """Input for productivity prediction"""
    study_hours_per_day: float = Field(..., ge=0, le=24)
    sleep_hours: float = Field(..., ge=0, le=24)
    stress_level: int = Field(..., ge=1, le=10)
    focus_score: int = Field(..., ge=1, le=100)


class TopFactor(BaseModel):
    factor: str
    impact: str
    value: float


class AiProductivityPrediction(BaseModel):
    """Output of productivity prediction"""
    predicted_score: float
    confidence: float
    top_factors: list[TopFactor]
    recommendation: str


class PeakStudyHour(BaseModel):
    hour: int
    average_productivity: float
    session_count: int


class PeakStudyHoursResponse(BaseModel):
    peak_hours: list[PeakStudyHour]
    best_hour: int
    best_productivity: float
    total_sessions_analyzed: int

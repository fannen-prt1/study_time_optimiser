"""
Initialize database using SQLAlchemy ORM models
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from app.database.connection import engine, Base
from app.models import (
    User, Subject, StudySession, Goal, Deadline,
    Achievement, StudyStreak, PomodoroSession,
    DailyWellness, RefreshToken, AIPrediction
)

# Drop all tables (careful in production!)
print("🗑️  Dropping existing tables...")
Base.metadata.drop_all(bind=engine)

# Create all tables from ORM models
print("📦 Creating tables from ORM models...")
Base.metadata.create_all(bind=engine)

print("✅ Database initialized successfully!")
print(f"   Database: {engine.url}")
print(f"   Tables created: {list(Base.metadata.tables.keys())}")

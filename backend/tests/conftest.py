"""
Pytest configuration and shared fixtures
"""
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.connection import Base
from app.database.dependencies import get_db
from app.models.user import User
from app.utils.password import hash_password


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator:
    """Create a fresh database session for each test"""
    # Import all models to ensure they're registered
    from app.models import (
        User, Subject, StudySession, Goal, Deadline,
        Achievement, StudyStreak, PomodoroSession,
        DailyWellness, RefreshToken, AIPrediction
    )
    
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    """Create a test client with database session override"""
    from app.main import app
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Use TestClient in synchronous mode
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session) -> User:
    """Create a test user"""
    user = User(
        email="test@example.com",
        password_hash=hash_password("TestPassword123"),
        full_name="Test User",
        age=25,
        student_type="college",
        is_verified=True,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def auth_headers(client, test_user) -> dict:
    """Get authentication headers with valid token"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPassword123"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def test_subject(client, auth_headers):
    """Create a test subject"""
    response = client.post(
        "/api/v1/subjects/",
        json={
            "name": "Mathematics",
            "color": "#FF5733",
            "icon": "📐",
            "description": "Advanced Calculus"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(scope="function")
def test_session(client, auth_headers, test_subject):
    """Create a test study session"""
    from datetime import datetime
    response = client.post(
        "/api/v1/sessions/",
        json={
            "subject_id": test_subject["id"],
            "planned_duration": 60,
            "notes": "Test session",
            "start_time": datetime.utcnow().isoformat()
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture(scope="function")
def test_goal(client, auth_headers, test_subject):
    """Create a test goal"""
    from datetime import date, timedelta
    response = client.post(
        "/api/v1/goals/",
        json={
            "subject_id": test_subject["id"],
            "title": "Study 20 hours",
            "description": "Monthly goal",
            "goal_type": "study_hours",
            "target_value": 20,
            "target_date": (date.today() + timedelta(days=30)).isoformat()
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    return response.json()

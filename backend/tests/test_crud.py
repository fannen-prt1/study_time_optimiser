"""
Tests for CRUD endpoints (Subjects, Sessions, Goals, Deadlines, Wellness)
"""
import pytest
from datetime import datetime, date, timedelta
from fastapi.testclient import TestClient


class TestSubjects:
    """Test subject CRUD operations"""
    
    def test_create_subject(self, client: TestClient, auth_headers):
        """Test creating a subject"""
        response = client.post(
            "/api/v1/subjects/",
            json={
                "name": "Physics",
                "color": "#3498db",
                "icon": "⚛️",
                "description": "Quantum Mechanics"
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Physics"
        assert data["color"] == "#3498db"
        assert "id" in data
    
    def test_get_all_subjects(self, client: TestClient, auth_headers, test_subject):
        """Test getting all subjects"""
        response = client.get("/api/v1/subjects/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_subject_by_id(self, client: TestClient, auth_headers, test_subject):
        """Test getting a specific subject"""
        response = client.get(
            f"/api/v1/subjects/{test_subject['id']}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_subject["id"]
        assert data["name"] == test_subject["name"]
    
    def test_update_subject(self, client: TestClient, auth_headers, test_subject):
        """Test updating a subject"""
        response = client.put(
            f"/api/v1/subjects/{test_subject['id']}",
            json={"description": "Updated description"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Updated description"
    
    def test_archive_subject(self, client: TestClient, auth_headers, test_subject):
        """Test archiving a subject"""
        response = client.post(
            f"/api/v1/subjects/{test_subject['id']}/archive",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_archived"] == True
    
    def test_delete_subject(self, client: TestClient, auth_headers, test_subject):
        """Test deleting a subject"""
        response = client.delete(
            f"/api/v1/subjects/{test_subject['id']}",
            headers=auth_headers
        )
        assert response.status_code == 204


class TestStudySessions:
    """Test study session CRUD operations"""
    
    def test_create_session(self, client: TestClient, auth_headers, test_subject):
        """Test creating a study session"""
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
        data = response.json()
        assert data["subject_id"] == test_subject["id"]
        assert data["planned_duration"] == 60
        assert data["status"] == "planned"
    
    def test_start_session(self, client: TestClient, auth_headers, test_session):
        """Test starting a session"""
        response = client.post(
            f"/api/v1/sessions/{test_session['id']}/start",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "in_progress"
    
    def test_complete_session(self, client: TestClient, auth_headers, test_session):
        """Test completing a session"""
        # Start first
        client.post(
            f"/api/v1/sessions/{test_session['id']}/start",
            headers=auth_headers
        )
        
        # Complete
        response = client.post(
            f"/api/v1/sessions/{test_session['id']}/complete",
            json={
                "actual_duration": 55,
                "productivity_score": 8,
                "focus_score": 7,
                "energy_level": 6,
                "difficulty_rating": 7,
                "mood_after": "satisfied",
                "session_feedback": "Good session"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["productivity_score"] == 8
    
    def test_get_all_sessions(self, client: TestClient, auth_headers, test_session):
        """Test getting all sessions"""
        response = client.get("/api/v1/sessions/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestGoals:
    """Test goal CRUD operations"""
    
    def test_create_goal(self, client: TestClient, auth_headers, test_subject):
        """Test creating a goal"""
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
        data = response.json()
        assert data["title"] == "Study 20 hours"
        assert data["target_value"] == 20
    
    def test_update_goal_progress(self, client: TestClient, auth_headers, test_goal):
        """Test updating goal progress"""
        response = client.post(
            f"/api/v1/goals/{test_goal['id']}/progress",
            json={"progress": 10.5},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["current_value"] == 10.5
    
    def test_mark_goal_achieved(self, client: TestClient, auth_headers, test_goal):
        """Test marking a goal as achieved"""
        response = client.post(
            f"/api/v1/goals/{test_goal['id']}/achieve",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_achieved"] == True


class TestDeadlines:
    """Test deadline CRUD operations"""
    
    def test_create_deadline(self, client: TestClient, auth_headers, test_subject):
        """Test creating a deadline"""
        response = client.post(
            "/api/v1/deadlines/",
            json={
                "subject_id": test_subject["id"],
                "title": "Final Exam",
                "description": "Comprehensive exam",
                "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
                "priority": "high"
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Final Exam"
        assert data["priority"] == "high"
    
    def test_mark_deadline_complete(self, client: TestClient, auth_headers, test_subject):
        """Test marking a deadline as complete"""
        # Create deadline
        create_response = client.post(
            "/api/v1/deadlines/",
            json={
                "subject_id": test_subject["id"],
                "title": "Assignment",
                "description": "Test",
                "due_date": datetime.now().isoformat(),
                "priority": "medium"
            },
            headers=auth_headers
        )
        deadline_id = create_response.json()["id"]
        
        # Mark complete
        response = client.post(
            f"/api/v1/deadlines/{deadline_id}/complete",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_completed"] == True


class TestWellness:
    """Test wellness CRUD operations"""
    
    def test_log_wellness(self, client: TestClient, auth_headers):
        """Test logging daily wellness"""
        response = client.post(
            "/api/v1/wellness/",
            json={
                "date": date.today().isoformat(),
                "sleep_hours": 7.5,
                "sleep_quality": 8,
                "energy_level": 7,
                "stress_level": 4,
                "mood": "good",
                "notes": "Feeling productive"
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["sleep_hours"] == 7.5
        assert data["mood"] == "good"
    
    def test_get_wellness_entries(self, client: TestClient, auth_headers):
        """Test getting wellness entries"""
        # Create entry first
        client.post(
            "/api/v1/wellness/",
            json={
                "date": date.today().isoformat(),
                "sleep_hours": 8,
                "sleep_quality": 9,
                "energy_level": 8,
                "stress_level": 3,
                "mood": "excellent"
            },
            headers=auth_headers
        )
        
        # Get entries
        response = client.get("/api/v1/wellness/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1


class TestUsers:
    """Test user profile operations"""
    
    def test_get_user_profile(self, client: TestClient, auth_headers):
        """Test getting user profile"""
        response = client.get("/api/v1/users/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "full_name" in data
    
    def test_update_user_profile(self, client: TestClient, auth_headers):
        """Test updating user profile"""
        response = client.put(
            "/api/v1/users/me",
            json={
                "full_name": "Updated Name",
                "age": 26
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["age"] == 26

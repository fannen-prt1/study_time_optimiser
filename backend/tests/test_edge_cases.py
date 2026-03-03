"""
Tests for edge cases and error handling
"""
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4


class TestEdgeCases:
    """Test edge cases and error scenarios"""
    
    def test_unauthorized_access(self, client: TestClient):
        """Test accessing protected endpoints without authentication"""
        endpoints = [
            "/api/v1/subjects/",
            "/api/v1/sessions/",
            "/api/v1/goals/",
            "/api/v1/deadlines/",
            "/api/v1/wellness/",
            "/api/v1/analytics/dashboard"
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 403
    
    def test_invalid_uuid(self, client: TestClient, auth_headers):
        """Test endpoints with invalid UUID"""
        response = client.get(
            "/api/v1/subjects/invalid-uuid",
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_nonexistent_resource(self, client: TestClient, auth_headers):
        """Test accessing non-existent resource"""
        fake_uuid = str(uuid4())
        response = client.get(
            f"/api/v1/subjects/{fake_uuid}",
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_invalid_email_format(self, client: TestClient):
        """Test registration with invalid email format"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "password": "Password123",
                "full_name": "User",
                "age": 20,
                "student_type": "college"
            }
        )
        assert response.status_code == 422
    
    def test_negative_age(self, client: TestClient):
        """Test registration with negative age"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "user@example.com",
                "password": "Password123",
                "full_name": "User",
                "age": -5,
                "student_type": "college"
            }
        )
        assert response.status_code == 422
    
    def test_invalid_date_format(self, client: TestClient, auth_headers):
        """Test wellness entry with invalid date"""
        response = client.post(
            "/api/v1/wellness/",
            json={
                "date": "not-a-date",
                "sleep_hours": 8,
                "sleep_quality": 9,
                "energy_level": 8,
                "stress_level": 3,
                "mood": "good"
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_out_of_range_scores(self, client: TestClient, auth_headers, test_session):
        """Test completing session with out-of-range scores"""
        client.post(f"/api/v1/sessions/{test_session['id']}/start", headers=auth_headers)
        
        response = client.post(
            f"/api/v1/sessions/{test_session['id']}/complete",
            json={
                "actual_duration": 60,
                "productivity_score": 15,  # Should be 1-10
                "focus_score": 7,
                "energy_level": 6,
                "difficulty_rating": 7,
                "mood_after": "satisfied",
                "session_feedback": "Session"
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_duplicate_wellness_entry(self, client: TestClient, auth_headers):
        """Test creating duplicate wellness entry for same date"""
        from datetime import date
        
        wellness_data = {
            "date": date.today().isoformat(),
            "sleep_hours": 8,
            "sleep_quality": 9,
            "energy_level": 8,
            "stress_level": 3,
            "mood": "good"
        }
        
        # First entry
        response1 = client.post("/api/v1/wellness/", json=wellness_data, headers=auth_headers)
        assert response1.status_code == 201
        
        # Second entry for same date (should update, not fail)
        response2 = client.post("/api/v1/wellness/", json=wellness_data, headers=auth_headers)
        assert response2.status_code == 201
    
    def test_update_other_users_resource(self, client: TestClient, test_subject):
        """Test updating another user's resource"""
        # Create second user
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "user2@example.com",
                "password": "Password123",
                "full_name": "User Two",
                "age": 23,
                "student_type": "college"
            }
        )
        
        # Login as second user
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "user2@example.com", "password": "Password123"}
        )
        
        # Manually verify second user since fixture creates verified user
        from app.models.user import User
        from app.database.connection import SessionLocal
        db = SessionLocal()
        user2 = db.query(User).filter(User.email == "user2@example.com").first()
        user2.is_verified = True
        db.commit()
        db.close()
        
        user2_token = login_response.json()["access_token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        
        # Try to access first user's subject
        response = client.get(
            f"/api/v1/subjects/{test_subject['id']}",
            headers=user2_headers
        )
        # Should not find it (404) because it belongs to different user
        assert response.status_code == 404
    
    def test_missing_required_fields(self, client: TestClient, auth_headers):
        """Test creating resource with missing required fields"""
        response = client.post(
            "/api/v1/subjects/",
            json={"name": "Subject"},  # Missing color
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_analytics_with_no_data(self, client: TestClient, auth_headers):
        """Test analytics endpoints with no study data"""
        response = client.get("/api/v1/analytics/dashboard", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        # Should return empty/zero values, not error
        assert data["study_time_stats"]["total_sessions"] == 0


class TestValidation:
    """Test input validation"""
    
    def test_sleep_hours_validation(self, client: TestClient, auth_headers):
        """Test sleep hours must be positive"""
        from datetime import date
        response = client.post(
            "/api/v1/wellness/",
            json={
                "date": date.today().isoformat(),
                "sleep_hours": -1,
                "sleep_quality": 8,
                "energy_level": 7,
                "stress_level": 4,
                "mood": "good"
            },
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_goal_target_value_validation(self, client: TestClient, auth_headers, test_subject):
        """Test goal target value must be positive"""
        from datetime import date, timedelta
        response = client.post(
            "/api/v1/goals/",
            json={
                "subject_id": test_subject["id"],
                "title": "Invalid Goal",
                "description": "Test",
                "goal_type": "study_hours",
                "target_value": -10,
                "target_date": (date.today() + timedelta(days=30)).isoformat()
            },
            headers=auth_headers
        )
        assert response.status_code == 422

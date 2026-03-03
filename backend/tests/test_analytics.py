"""
Tests for analytics endpoints
"""
import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient


class TestAnalytics:
    """Test analytics endpoints"""
    
    def test_get_streak_info(self, client: TestClient, auth_headers):
        """Test getting streak information"""
        response = client.get("/api/v1/analytics/streak", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "current_streak" in data
        assert "longest_streak" in data
        assert "total_study_days" in data
    
    def test_get_study_time_stats(self, client: TestClient, auth_headers):
        """Test getting study time statistics"""
        response = client.get("/api/v1/analytics/study-time", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_minutes" in data
        assert "total_sessions" in data
        assert "average_productivity_score" in data
        assert "completion_rate" in data
    
    def test_get_subject_stats(self, client: TestClient, auth_headers, test_subject):
        """Test getting subject statistics"""
        response = client.get("/api/v1/analytics/subjects", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_productivity_trends(self, client: TestClient, auth_headers):
        """Test getting productivity trends"""
        response = client.get(
            "/api/v1/analytics/productivity-trends?days=7",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 7  # Should return 7 days of data
    
    def test_get_goal_progress(self, client: TestClient, auth_headers):
        """Test getting goal progress"""
        response = client.get("/api/v1/analytics/goals/progress", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_wellness_correlation(self, client: TestClient, auth_headers):
        """Test getting wellness correlation"""
        response = client.get(
            "/api/v1/analytics/wellness-correlation?days=7",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "average_sleep_hours" in data
        assert "average_productivity" in data
        assert "optimal_sleep_range" in data
    
    def test_get_dashboard_analytics(self, client: TestClient, auth_headers):
        """Test getting complete dashboard analytics"""
        response = client.get(
            "/api/v1/analytics/dashboard?days=30",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "study_time_stats" in data
        assert "subject_stats" in data
        assert "productivity_trends" in data
        assert "goal_progress" in data
        assert "streak_info" in data
        assert "wellness_correlation" in data
        assert "upcoming_deadlines" in data
    
    def test_analytics_with_date_filters(self, client: TestClient, auth_headers):
        """Test analytics with custom date filters"""
        start_date = (date.today() - timedelta(days=7)).isoformat()
        end_date = date.today().isoformat()
        
        response = client.get(
            f"/api/v1/analytics/study-time?start_date={start_date}&end_date={end_date}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_minutes" in data

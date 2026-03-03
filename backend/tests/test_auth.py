"""
Tests for authentication endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_user(self, client: TestClient):
        """Test user registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "SecurePass123",
                "full_name": "New User",
                "age": 22,
                "student_type": "college"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["full_name"] == "New User"
        assert data["age"] == 22
        assert "id" in data
    
    def test_register_duplicate_email(self, client: TestClient, test_user):
        """Test registration with duplicate email"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "Password123",
                "full_name": "Duplicate User",
                "age": 25,
                "student_type": "college"
            }
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_register_weak_password(self, client: TestClient):
        """Test registration with weak password"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "user@example.com",
                "password": "weak",
                "full_name": "User",
                "age": 20,
                "student_type": "college"
            }
        )
        assert response.status_code == 422
    
    def test_login_success(self, client: TestClient, test_user):
        """Test successful login"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "TestPassword123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 1800
    
    def test_login_wrong_password(self, client: TestClient, test_user):
        """Test login with wrong password"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "WrongPassword123"
            }
        )
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with non-existent email"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "Password123"
            }
        )
        assert response.status_code == 401
    
    def test_get_current_user(self, client: TestClient, auth_headers, test_user):
        """Test getting current user profile"""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test User"
        assert data["age"] == 25
    
    def test_get_current_user_unauthenticated(self, client: TestClient):
        """Test getting current user without authentication"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 403
    
    def test_get_current_user_invalid_token(self, client: TestClient):
        """Test getting current user with invalid token"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 403
    
    def test_refresh_token(self, client: TestClient, test_user):
        """Test token refresh"""
        # Login first
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "TestPassword123"
            }
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
    
    def test_logout(self, client: TestClient, auth_headers):
        """Test logout"""
        # Get refresh token first
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "TestPassword123"
            }
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # Logout
        response = client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": refresh_token},
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "successfully logged out" in response.json()["message"].lower()
    
    def test_change_password(self, client: TestClient, auth_headers):
        """Test password change"""
        response = client.post(
            "/api/v1/auth/change-password",
            json={
                "current_password": "TestPassword123",
                "new_password": "NewPassword123"
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        
        # Verify new password works
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "NewPassword123"
            }
        )
        assert login_response.status_code == 200
    
    def test_change_password_wrong_current(self, client: TestClient, auth_headers):
        """Test password change with wrong current password"""
        response = client.post(
            "/api/v1/auth/change-password",
            json={
                "current_password": "WrongPassword123",
                "new_password": "NewPassword123"
            },
            headers=auth_headers
        )
        assert response.status_code == 400

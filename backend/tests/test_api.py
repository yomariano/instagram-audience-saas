import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.main import app

client = TestClient(app)

class TestAPI:
    
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Instagram Audience Analysis API"}
    
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    @patch('app.api.routes.start_scraping_job')
    def test_add_instagram_account_success(self, mock_start_job):
        mock_start_job.return_value = "test_job_id"
        
        response = client.post(
            "/api/v1/accounts",
            json={"username": "test_username"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Analysis started for @test_username"
        assert data["job_id"] == "test_job_id"
    
    def test_add_instagram_account_missing_username(self):
        response = client.post(
            "/api/v1/accounts",
            json={}
        )
        
        assert response.status_code == 400
        assert "Username is required" in response.json()["detail"]
    
    @patch('app.api.routes.get_analysis_results')
    def test_get_account_analysis(self, mock_get_results):
        mock_results = {
            "username": "test_user",
            "total_comments": 150,
            "demographics": {"gender_split": {"male": 45, "female": 55}},
            "status": "completed"
        }
        mock_get_results.return_value = mock_results
        
        response = client.get("/api/v1/accounts/test_user/analysis")
        
        assert response.status_code == 200
        assert response.json() == mock_results
    
    def test_get_demographics(self):
        response = client.get("/api/v1/accounts/test_user/demographics")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check structure
        assert "gender_split" in data
        assert "age_distribution" in data
        assert "account_types" in data
        
        # Check values
        assert data["gender_split"]["male"] == 45
        assert data["gender_split"]["female"] == 55
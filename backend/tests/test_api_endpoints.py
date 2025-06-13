"""
Test API endpoints using FastAPI TestClient
"""
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.mark.api
class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_health_endpoint(self, test_client):
        """Test health check endpoint"""
        response = test_client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_root_endpoint(self, test_client):
        """Test root endpoint"""
        response = test_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "CitiBike" in data["message"]
    
    def test_stations_endpoint(self, test_client, populated_test_db):
        """Test stations endpoint returns station list"""
        response = test_client.get("/api/stations")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check station structure
        station = data[0]
        assert "station_id" in station
        assert "name" in station
        assert "latitude" in station
        assert "longitude" in station
    
    def test_probability_endpoint_valid_request(self, test_client, populated_test_db):
        """Test probability endpoint with valid request"""
        request_data = {
            "home_station_id": "Test Station 1",  # Use station name from mapping
            "riding_frequency": 5,
            "time_pattern": "weekday"
        }
        
        response = test_client.post("/api/probability", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "probability" in data
        assert "confidence_interval" in data
        assert "explanation" in data
        assert isinstance(data["probability"], (int, float))
        assert 0 <= data["probability"] <= 1
    
    def test_probability_endpoint_with_station_name(self, test_client, populated_test_db):
        """Test probability endpoint with station name instead of UUID"""
        request_data = {
            "home_station_id": "Test Station 1",  # Station name
            "riding_frequency": 3,
            "time_pattern": "weekend"
        }
        
        response = test_client.post("/api/probability", json=request_data)
        assert response.status_code == 200
        data = response.json()
        
        assert "probability" in data
        assert "confidence_interval" in data
        assert "explanation" in data
        assert isinstance(data["probability"], (int, float))
    
    def test_probability_endpoint_invalid_station(self, test_client, populated_test_db):
        """Test probability endpoint with invalid station"""
        request_data = {
            "home_station_id": "nonexistent_station",
            "riding_frequency": 5,
            "time_pattern": "weekday"
        }
        
        response = test_client.post("/api/probability", json=request_data)
        assert response.status_code == 400  # Changed from 404 to 400 (Bad Request)
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_probability_endpoint_invalid_frequency(self, test_client, populated_test_db):
        """Test probability endpoint with invalid riding frequency"""
        request_data = {
            "home_station_id": "Test Station 1",  # Use correct station name
            "riding_frequency": -1,  # Invalid negative frequency
            "time_pattern": "weekday"
        }
        
        response = test_client.post("/api/probability", json=request_data)
        assert response.status_code == 400  # Bad Request for business logic validation
        data = response.json()
        assert "detail" in data
        assert "positive number" in data["detail"]
    
    def test_probability_endpoint_invalid_time_pattern(self, test_client, populated_test_db):
        """Test probability endpoint with invalid time pattern"""
        request_data = {
            "home_station_id": "Test Station 1",  # Use correct station name
            "riding_frequency": 5,
            "time_pattern": "invalid_pattern"
        }
        
        response = test_client.post("/api/probability", json=request_data)
        assert response.status_code == 400  # Bad Request for business logic validation
        data = response.json()
        assert "detail" in data
        assert "Time pattern must be" in data["detail"]
    
    def test_probability_endpoint_missing_fields(self, test_client, populated_test_db):
        """Test probability endpoint with missing required fields"""
        # Missing riding_frequency
        request_data = {
            "home_station_id": "Test Station 1",  # Use correct station name
            "time_pattern": "weekday"
        }
        
        response = test_client.post("/api/probability", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_probability_endpoint_different_time_patterns(self, test_client, populated_test_db):
        """Test probability endpoint with different time patterns"""
        patterns = ["weekday", "weekend", "both"]
        
        for pattern in patterns:
            request_data = {
                "home_station_id": "Test Station 1",  # Use correct station name
                "riding_frequency": 5,
                "time_pattern": pattern
            }
            
            response = test_client.post("/api/probability", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert "probability" in data
    
    def test_probability_endpoint_different_frequencies(self, test_client, populated_test_db):
        """Test probability endpoint with different riding frequencies"""
        frequencies = [1, 3, 5, 7, 10]
        
        for freq in frequencies:
            request_data = {
                "home_station_id": "Test Station 1",  # Use correct station name
                "riding_frequency": freq,
                "time_pattern": "weekday"
            }
            
            response = test_client.post("/api/probability", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert "probability" in data
    
    def test_probability_endpoint_different_stations(self, test_client, populated_test_db):
        """Test probability endpoint with different stations"""
        stations = ["Test Station 1", "Test Station 2", "Test Station 3"]  # Use correct station names
        
        for station in stations:
            request_data = {
                "home_station_id": station,
                "riding_frequency": 5,
                "time_pattern": "weekday"
            }
            
            response = test_client.post("/api/probability", json=request_data)
            assert response.status_code == 200
            data = response.json()
            assert "probability" in data
    
    def test_api_response_format_consistency(self, test_client, populated_test_db):
        """Test that API responses have consistent format"""
        request_data = {
            "home_station_id": "Test Station 1",  # Use correct station name
            "riding_frequency": 5,
            "time_pattern": "weekday"
        }
        
        response = test_client.post("/api/probability", json=request_data)
        data = response.json()
        
        # Check all required fields are present
        required_fields = ["probability", "confidence_interval", "explanation"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Check data types
        assert isinstance(data["probability"], (int, float))
        assert isinstance(data["confidence_interval"], str)
        assert isinstance(data["explanation"], str)
        
        # Check probability is in valid range
        assert 0 <= data["probability"] <= 1
        
        # Check confidence interval format
        assert "to" in data["confidence_interval"].lower() or "%" in data["confidence_interval"]
    
    def test_probability_endpoint_with_uuid(self, test_client, populated_test_db):
        """Test probability endpoint with UUID directly"""
        request_data = {
            "home_station_id": "test-uuid-1",  # UUID from station mapping
            "riding_frequency": 2,
            "time_pattern": "both"
        }

        response = test_client.post("/api/probability", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert "probability" in data
        assert "confidence_interval" in data
        assert "explanation" in data 
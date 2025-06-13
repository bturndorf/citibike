"""
Test probability calculation logic
"""
import pytest
from prob_calc import CitiBikeProbabilityCalculator, calculate_probability
from models import Station, Trip, StationMapping

@pytest.mark.probability
class TestProbabilityCalculations:
    """Test probability calculation logic"""
    
    def test_probability_calculator_initialization(self, probability_calculator):
        """Test probability calculator initialization"""
        assert probability_calculator is not None
        assert hasattr(probability_calculator, 'db_session')
    
    def test_load_station_statistics(self, probability_calculator, populated_test_db):
        """Test loading station statistics"""
        stats = probability_calculator.load_station_statistics()
        assert isinstance(stats, dict)
        assert len(stats) > 0
        
        # Check structure of station stats
        for station_id, station_data in stats.items():
            assert "name" in station_data
            assert "total_trips" in station_data
            assert "unique_bikes" in station_data
            assert isinstance(station_data["total_trips"], int)
            assert isinstance(station_data["unique_bikes"], int)
    
    def test_calculate_probability_basic(self, probability_calculator, populated_test_db):
        """Test basic probability calculation"""
        result = probability_calculator.calculate_bike_movement_probability(
            home_station_id="Test Station 1",  # Use station name
            riding_frequency=5,
            time_pattern="weekday"
        )
        
        # Check that result contains expected fields
        assert "probability" in result
        assert "confidence_interval" in result
        assert "explanation" in result
        assert "station_info" in result
        
        # Check data types
        assert isinstance(result["probability"], (int, float))
        assert isinstance(result["confidence_interval"], str)
        assert isinstance(result["explanation"], str)
        assert isinstance(result["station_info"], dict)
        
        # Check probability is in valid range
        assert 0 <= result["probability"] <= 1
    
    def test_calculate_probability_with_station_name(self, probability_calculator, populated_test_db):
        """Test probability calculation with station name"""
        result = calculate_probability(
            db_session=populated_test_db,
            home_station_id="Test Station 1",  # Station name
            riding_frequency=3,
            time_pattern="weekend"
        )
        
        assert isinstance(result, dict)
        assert "probability" in result
        assert 0 <= result["probability"] <= 1
    
    def test_calculate_probability_with_uuid(self, probability_calculator, populated_test_db):
        """Test probability calculation with UUID"""
        result = calculate_probability(
            db_session=populated_test_db,
            home_station_id="test-uuid-1",  # UUID
            riding_frequency=5,
            time_pattern="weekday"
        )
        
        assert isinstance(result, dict)
        assert "probability" in result
        assert 0 <= result["probability"] <= 1
    
    def test_probability_different_frequencies(self, probability_calculator, populated_test_db):
        """Test probability calculation with different frequencies"""
        frequencies = [1, 3, 5, 7, 10]
        results = []
        
        for freq in frequencies:
            result = probability_calculator.calculate_bike_movement_probability(
                home_station_id="Test Station 1",  # Use station name
                riding_frequency=freq,
                time_pattern="weekday"
            )
            results.append(result)
            assert "probability" in result
            assert 0 <= result["probability"] <= 1
        
        # Check that different frequencies produce different results
        probabilities = [r["probability"] for r in results]
        assert len(set(probabilities)) > 1  # At least some different probabilities
    
    def test_probability_different_time_patterns(self, probability_calculator, populated_test_db):
        """Test probability calculation with different time patterns"""
        patterns = ["weekday", "weekend", "both"]
        
        for pattern in patterns:
            result = probability_calculator.calculate_bike_movement_probability(
                home_station_id="Test Station 1",  # Use station name
                riding_frequency=5,
                time_pattern=pattern
            )
            assert "probability" in result
            assert 0 <= result["probability"] <= 1
    
    def test_probability_different_stations(self, probability_calculator, populated_test_db):
        """Test probability calculation with different stations"""
        stations = ["Test Station 1", "Test Station 2", "Test Station 3"]  # Use station names
        
        for station in stations:
            result = probability_calculator.calculate_bike_movement_probability(
                home_station_id=station,
                riding_frequency=5,
                time_pattern="weekday"
            )
            assert "probability" in result
            assert 0 <= result["probability"] <= 1
    
    def test_get_uuid_by_station_name(self, probability_calculator, populated_test_db):
        """Test UUID lookup by station name"""
        # Test with existing station name
        uuid = probability_calculator.get_uuid_by_station_name("Test Station 1")
        assert uuid == "test-uuid-1"
        
        # Test with non-existent station name
        with pytest.raises(ValueError, match="Station 'Nonexistent Station' not found in database"):
            probability_calculator.get_uuid_by_station_name("Nonexistent Station")
    
    def test_is_uuid_format(self, probability_calculator):
        """Test UUID format detection"""
        # Valid UUID format
        assert probability_calculator.is_uuid_format("test-uuid-1") == True
        assert probability_calculator.is_uuid_format("66dc120f-0aca-11e7-82f6-3863bb44ef7c") == True
        
        # Invalid UUID format
        assert probability_calculator.is_uuid_format("test_station_1") == False
        assert probability_calculator.is_uuid_format("Test Station 1") == False
        assert probability_calculator.is_uuid_format("") == False
    
    def test_probability_edge_cases(self, probability_calculator, populated_test_db):
        """Test probability calculation edge cases"""
        # Very low frequency
        result = probability_calculator.calculate_bike_movement_probability(
            home_station_id="Test Station 1",  # Use station name
            riding_frequency=1,
            time_pattern="weekday"
        )
        assert "probability" in result
        assert 0 <= result["probability"] <= 1
        
        # Test with invalid inputs
        with pytest.raises(ValueError, match="Riding frequency must be a positive number"):
            probability_calculator.calculate_bike_movement_probability(
                home_station_id="Test Station 1",
                riding_frequency=0,
                time_pattern="weekday"
            )
        
        with pytest.raises(ValueError, match="Time pattern must be"):
            probability_calculator.calculate_bike_movement_probability(
                home_station_id="Test Station 1",
                riding_frequency=5,
                time_pattern="invalid"
            )
    
    def test_probability_mathematical_consistency(self, probability_calculator, populated_test_db):
        """Test mathematical consistency of probability calculations"""
        # Same parameters should give same results
        result1 = probability_calculator.calculate_bike_movement_probability(
            home_station_id="Test Station 1",
            riding_frequency=5,
            time_pattern="weekday"
        )
        
        result2 = probability_calculator.calculate_bike_movement_probability(
            home_station_id="Test Station 1",
            riding_frequency=5,
            time_pattern="weekday"
        )
        
        assert abs(result1["probability"] - result2["probability"]) < 0.0001
    
    def test_confidence_interval_format(self, probability_calculator, populated_test_db):
        """Test confidence interval format"""
        result = probability_calculator.calculate_bike_movement_probability(
            home_station_id="Test Station 1",
            riding_frequency=5,
            time_pattern="weekday"
        )
        
        confidence_interval = result["confidence_interval"]
        assert isinstance(confidence_interval, str)
        assert len(confidence_interval) > 0
        
        # Should contain percentage or range information
        assert any(char in confidence_interval for char in ["%", "to", "-"])
    
    def test_explanation_content(self, probability_calculator, populated_test_db):
        """Test explanation content"""
        result = probability_calculator.calculate_bike_movement_probability(
            home_station_id="Test Station 1",
            riding_frequency=5,
            time_pattern="weekday"
        )
        
        explanation = result["explanation"]
        assert isinstance(explanation, str)
        assert len(explanation) > 10  # Should have meaningful content
        
        # Should mention key concepts
        explanation_lower = explanation.lower()
        assert any(word in explanation_lower for word in ["bike", "station", "probability", "chance"])
    
    def test_station_info_in_result(self, probability_calculator, populated_test_db):
        """Test that station info is included in result when available"""
        result = probability_calculator.calculate_bike_movement_probability(
            home_station_id="Test Station 1",
            riding_frequency=5,
            time_pattern="weekday"
        )
        
        if "station_info" in result:
            station_info = result["station_info"]
            assert "name" in station_info
            assert "total_trips" in station_info
            assert "unique_bikes" in station_info
            assert isinstance(station_info["total_trips"], int)
            assert isinstance(station_info["unique_bikes"], int)
    
    def test_error_handling_invalid_station(self, probability_calculator, populated_test_db):
        """Test error handling for invalid station"""
        with pytest.raises(Exception):
            probability_calculator.calculate_bike_movement_probability(
                home_station_id="nonexistent_station",
                riding_frequency=5,
                time_pattern="weekday"
            )
    
    def test_error_handling_invalid_frequency(self, probability_calculator, populated_test_db):
        """Test error handling for invalid frequency"""
        with pytest.raises(Exception):
            probability_calculator.calculate_bike_movement_probability(
                home_station_id="Test Station 1",
                riding_frequency=-1,
                time_pattern="weekday"
            )
    
    def test_error_handling_invalid_time_pattern(self, probability_calculator, populated_test_db):
        """Test error handling for invalid time pattern"""
        with pytest.raises(Exception):
            probability_calculator.calculate_bike_movement_probability(
                home_station_id="Test Station 1",
                riding_frequency=5,
                time_pattern="invalid_pattern"
            ) 
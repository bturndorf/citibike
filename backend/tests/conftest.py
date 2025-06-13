import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

"""
Pytest configuration and fixtures for CitiBike backend tests
"""
import pytest
import os
import tempfile
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app, get_db
from models import Base
from prob_calc import CitiBikeProbabilityCalculator
import logging
from sqlalchemy import text

# Configure logging for tests
logging.basicConfig(level=logging.WARNING)

@pytest.fixture(scope="session")
def test_database_url():
    """Get test database URL from environment or use PostgreSQL"""
    return os.getenv("TEST_DATABASE_URL", "postgresql://localhost:5432/citibike_test")

@pytest.fixture(scope="session")
def test_engine(test_database_url):
    """Create test database engine"""
    # Always use PostgreSQL for tests (no SQLite fallback)
    engine = create_engine(test_database_url)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Clean up any existing test data at session start
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM trips"))
        conn.execute(text("DELETE FROM station_mapping"))
        conn.execute(text("DELETE FROM stations"))
        conn.commit()
    
    yield engine
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_db_session(test_engine):
    """Create test database session"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    
    yield session
    
    # Rollback and close
    session.rollback()
    session.close()

@pytest.fixture(scope="function")
def test_client(test_db_session):
    """Create FastAPI test client with proper configuration"""
    # Ensure test environment is set
    os.environ["TESTING"] = "true"
    os.environ["ENVIRONMENT"] = "test"
    
    # Override the database dependency to use our test session
    def override_get_db():
        yield test_db_session
    
    from main import app
    app.dependency_overrides = {}
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    client = TestClient(app)
    
    yield client
    
    # Clean up dependency overrides
    app.dependency_overrides = {}
    
    # Clean up any test-specific environment variables
    if "TESTING" in os.environ:
        del os.environ["TESTING"]
    if "ENVIRONMENT" in os.environ:
        del os.environ["ENVIRONMENT"]

@pytest.fixture(scope="function")
def probability_calculator(test_db_session):
    """Create probability calculator instance for testing"""
    return CitiBikeProbabilityCalculator(test_db_session)

@pytest.fixture(scope="function")
def sample_stations():
    """Sample station data for testing"""
    return [
        {
            "station_id": "test-uuid-1",
            "name": "Test Station 1",
            "latitude": 40.7589,
            "longitude": -73.9851
        },
        {
            "station_id": "test-uuid-2", 
            "name": "Test Station 2",
            "latitude": 40.7505,
            "longitude": -73.9934
        },
        {
            "station_id": "test-uuid-3",
            "name": "Test Station 3", 
            "latitude": 40.7484,
            "longitude": -73.9857
        }
    ]

@pytest.fixture(scope="function")
def sample_trips():
    """Sample trip data for testing"""
    return [
        {
            "bike_id": "bike_001",
            "start_station_id": "test_station_1",
            "end_station_id": "test_station_2",
            "started_at": datetime(2024, 1, 1, 8, 0, 0),
            "ended_at": datetime(2024, 1, 1, 8, 15, 0)
        },
        {
            "bike_id": "bike_002",
            "start_station_id": "test_station_2", 
            "end_station_id": "test_station_3",
            "started_at": datetime(2024, 1, 1, 9, 0, 0),
            "ended_at": datetime(2024, 1, 1, 9, 12, 0)
        },
        {
            "bike_id": "bike_001",  # Same bike as first trip
            "start_station_id": "test_station_3",
            "end_station_id": "test_station_1", 
            "started_at": datetime(2024, 1, 1, 10, 0, 0),
            "ended_at": datetime(2024, 1, 1, 10, 18, 0)
        }
    ]

@pytest.fixture(scope="function")
def sample_station_mappings():
    """Sample station mapping data for testing"""
    return [
        {
            "uuid_station_id": "test-uuid-1",
            "numeric_station_id": "test_station_1",
            "station_name": "Test Station 1"
        },
        {
            "uuid_station_id": "test-uuid-2",
            "numeric_station_id": "test_station_2", 
            "station_name": "Test Station 2"
        },
        {
            "uuid_station_id": "test-uuid-3",
            "numeric_station_id": "test_station_3",
            "station_name": "Test Station 3"
        }
    ]

@pytest.fixture(scope="function")
def populated_test_db(test_db_session, sample_stations, sample_trips, sample_station_mappings):
    """Populate test database with sample data"""
    from models import Station, Trip, StationMapping
    
    # Clear existing data first to prevent unique constraint violations
    test_db_session.query(Trip).delete()
    test_db_session.query(StationMapping).delete()
    test_db_session.query(Station).delete()
    test_db_session.commit()
    
    # Add sample stations
    for station_data in sample_stations:
        station = Station(**station_data)
        test_db_session.add(station)
    
    # Add sample station mappings
    for mapping_data in sample_station_mappings:
        mapping = StationMapping(**mapping_data)
        test_db_session.add(mapping)
    
    # Add sample trips
    for trip_data in sample_trips:
        trip = Trip(**trip_data)
        test_db_session.add(trip)
    
    test_db_session.commit()
    
    yield test_db_session
    
    # Cleanup is handled by test_db_session fixture 
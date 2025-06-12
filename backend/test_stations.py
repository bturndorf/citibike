#!/usr/bin/env python3
"""
Test script to load stations and trips data into Railway PostgreSQL for full frontend testing
"""

import os
import logging
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_data():
    """Create comprehensive test data for full frontend testing"""
    
    logger.info("🧪 Creating comprehensive test data...")
    
    try:
        load_dotenv()
        database_url = os.getenv("DATABASE_URL")
        
        engine = create_engine(database_url)
        
        # Create tables if they don't exist
        with engine.connect() as conn:
            logger.info("🏗️ Creating tables...")
            
            # Stations table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS stations (
                    id SERIAL PRIMARY KEY,
                    station_id VARCHAR(50) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    latitude DECIMAL(10, 8) NOT NULL,
                    longitude DECIMAL(11, 8) NOT NULL
                )
            """))
            
            # Trips table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS trips (
                    id SERIAL PRIMARY KEY,
                    bike_id VARCHAR(50) NOT NULL,
                    start_station_id VARCHAR(50) NOT NULL,
                    end_station_id VARCHAR(50) NOT NULL,
                    started_at TIMESTAMP,
                    ended_at TIMESTAMP
                )
            """))
            
            conn.commit()
            logger.info("✅ Tables created successfully")
        
        # Clear existing data
        with engine.connect() as conn:
            logger.info("🧹 Clearing existing data...")
            conn.execute(text("DELETE FROM trips"))
            conn.execute(text("DELETE FROM stations"))
            conn.commit()
        
        # Insert test stations
        test_stations = [
            {"station_id": "test_1", "name": "Times Square Station", "latitude": 40.7589, "longitude": -73.9851},
            {"station_id": "test_2", "name": "Central Park Station", "latitude": 40.7505, "longitude": -73.9934},
            {"station_id": "test_3", "name": "Union Square Station", "latitude": 40.7484, "longitude": -73.9857},
            {"station_id": "test_4", "name": "Brooklyn Bridge Station", "latitude": 40.7061, "longitude": -73.9969},
            {"station_id": "test_5", "name": "High Line Station", "latitude": 40.7484, "longitude": -74.0047}
        ]
        
        with engine.connect() as conn:
            for station in test_stations:
                conn.execute(text("""
                    INSERT INTO stations (station_id, name, latitude, longitude)
                    VALUES (:station_id, :name, :latitude, :longitude)
                """), station)
            conn.commit()
            logger.info(f"✅ Inserted {len(test_stations)} test stations")
        
        # Create realistic trip data
        logger.info("🚲 Creating test trip data...")
        
        # Generate trip data with realistic patterns
        base_time = datetime.now() - timedelta(days=30)  # Start 30 days ago
        trips = []
        
        # Create bikes that return to the same stations (for realistic probability calculations)
        bike_patterns = [
            # Bike 1: Frequently returns to Times Square
            {"bike_id": "BIKE001", "home_station": "test_1", "return_rate": 0.7},
            {"bike_id": "BIKE002", "home_station": "test_1", "return_rate": 0.6},
            {"bike_id": "BIKE003", "home_station": "test_2", "return_rate": 0.8},
            {"bike_id": "BIKE004", "home_station": "test_2", "return_rate": 0.5},
            {"bike_id": "BIKE005", "home_station": "test_3", "return_rate": 0.4},
            {"bike_id": "BIKE006", "home_station": "test_3", "return_rate": 0.3},
            {"bike_id": "BIKE007", "home_station": "test_4", "return_rate": 0.9},
            {"bike_id": "BIKE008", "home_station": "test_5", "return_rate": 0.2},
        ]
        
        # Generate trips for each bike
        for pattern in bike_patterns:
            bike_id = pattern["bike_id"]
            home_station = pattern["home_station"]
            return_rate = pattern["return_rate"]
            
            current_time = base_time
            
            # Generate 10-20 trips per bike over 30 days
            num_trips = 15
            
            for i in range(num_trips):
                # Start from home station
                start_station = home_station
                
                # Choose destination (sometimes return to home, sometimes go elsewhere)
                if i > 0 and i % 3 == 0 and return_rate > 0.5:  # Return to home station
                    end_station = home_station
                else:
                    # Go to a different station
                    other_stations = [s["station_id"] for s in test_stations if s["station_id"] != home_station]
                    end_station = other_stations[i % len(other_stations)]
                
                # Generate realistic timestamps
                trip_start = current_time + timedelta(hours=i*2, minutes=i*15)  # Every 2 hours
                trip_duration = timedelta(minutes=15 + (i % 20))  # 15-35 minutes
                trip_end = trip_start + trip_duration
                
                trips.append({
                    "bike_id": bike_id,
                    "start_station_id": start_station,
                    "end_station_id": end_station,
                    "started_at": trip_start,
                    "ended_at": trip_end
                })
                
                current_time = trip_end + timedelta(hours=1)  # 1 hour gap between trips
        
        # Insert trips in batches
        with engine.connect() as conn:
            batch_size = 50
            for i in range(0, len(trips), batch_size):
                batch = trips[i:i+batch_size]
                for trip in batch:
                    conn.execute(text("""
                        INSERT INTO trips (bike_id, start_station_id, end_station_id, started_at, ended_at)
                        VALUES (:bike_id, :start_station_id, :end_station_id, :started_at, :ended_at)
                    """), trip)
                conn.commit()
                logger.info(f"✅ Inserted trips {i+1} to {min(i+batch_size, len(trips))}")
        
        # Verify data
        with engine.connect() as conn:
            station_count = conn.execute(text("SELECT COUNT(*) FROM stations")).scalar()
            trip_count = conn.execute(text("SELECT COUNT(*) FROM trips")).scalar()
            unique_bikes = conn.execute(text("SELECT COUNT(DISTINCT bike_id) FROM trips")).scalar()
        
        logger.info(f"📊 Final database statistics:")
        logger.info(f"  Stations: {station_count}")
        logger.info(f"  Trips: {trip_count}")
        logger.info(f"  Unique Bikes: {unique_bikes}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    create_test_data() 
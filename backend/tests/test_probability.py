#!/usr/bin/env python3
"""
Test script for the CitiBike probability calculation module
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from prob_calc import calculate_probability
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_probability_calculation():
    """Test the probability calculation with sample data"""
    
    # Database connection (using SQLite for testing)
    DATABASE_URL = "sqlite:///./dev.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    
    try:
        # Test parameters using actual station IDs from sample data
        test_cases = [
            {
                "home_station_id": "station_001",  # Times Square
                "riding_frequency": 5,
                "time_pattern": "weekday",
                "description": "Weekday commuter at Times Square"
            },
            {
                "home_station_id": "station_002",  # Central Park
                "riding_frequency": 2,
                "time_pattern": "weekend",
                "description": "Weekend rider at Central Park"
            },
            {
                "home_station_id": "station_003",  # Union Square
                "riding_frequency": 7,
                "time_pattern": "both",
                "description": "Daily rider at Union Square"
            }
        ]
        
        print("Testing CitiBike Probability Calculation")
        print("=" * 50)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest Case {i}: {test_case['description']}")
            print("-" * 30)
            
            try:
                result = calculate_probability(
                    db_session=db,
                    home_station_id=test_case["home_station_id"],
                    riding_frequency=test_case["riding_frequency"],
                    time_pattern=test_case["time_pattern"]
                )
                
                print(f"Station: {test_case['home_station_id']}")
                print(f"Riding Frequency: {test_case['riding_frequency']} rides/week")
                print(f"Time Pattern: {test_case['time_pattern']}")
                print(f"Probability: {result['probability']:.1%}")
                print(f"Confidence Interval: {result['confidence_interval']}")
                print(f"Explanation: {result['explanation']}")
                
                if result.get('station_info'):
                    station = result['station_info']
                    print(f"Station Info: {station['name']} ({station['total_trips']} trips, {station['unique_bikes']} bikes)")
                
            except Exception as e:
                print(f"Error in test case {i}: {e}")
                logger.error(f"Test case {i} failed: {e}")
        
        print("\n" + "=" * 50)
        print("Testing completed!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"Test failed: {e}")
    
    finally:
        db.close()

def test_station_loading():
    """Test station statistics loading"""
    
    DATABASE_URL = "sqlite:///./dev.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    
    try:
        from prob_calc import CitiBikeProbabilityCalculator
        
        calculator = CitiBikeProbabilityCalculator(db)
        station_stats = calculator.load_station_statistics()
        
        print(f"\nLoaded {len(station_stats)} stations")
        
        if station_stats:
            # Show top 5 stations by trip count
            sorted_stations = sorted(station_stats.values(), key=lambda x: x['total_trips'], reverse=True)
            
            print("\nTop 5 stations by trip count:")
            for i, station in enumerate(sorted_stations[:5], 1):
                print(f"{i}. {station['name']} - {station['total_trips']} trips, {station['unique_bikes']} bikes")
        
    except Exception as e:
        logger.error(f"Station loading test failed: {e}")
        print(f"Station loading test failed: {e}")
    
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting CitiBike Probability Tests...")
    
    # Test station loading first
    test_station_loading()
    
    # Test probability calculation
    test_probability_calculation() 
#!/usr/bin/env python3
"""
Script to create sample data for testing the CitiBike probability calculation
"""

import sqlite3
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample stations and trips data"""
    
    # Connect to database
    conn = sqlite3.connect('dev.db')
    cursor = conn.cursor()
    
    try:
        # Create sample stations
        sample_stations = [
            ("station_001", "Times Square - 7th Ave & 42nd St", 40.7589, -73.9851),
            ("station_002", "Central Park - 5th Ave & 59th St", 40.7645, -73.9741),
            ("station_003", "Union Square - 4th Ave & 14th St", 40.7359, -73.9911),
            ("station_004", "Brooklyn Bridge - Tillary St & Adams St", 40.6955, -73.9877),
            ("station_005", "Williamsburg - Bedford Ave & N 7th St", 40.7172, -73.9568),
            ("station_006", "Astoria - 31st St & 31st Ave", 40.7642, -73.9235),
            ("station_007", "Harlem - 125th St & Lenox Ave", 40.8045, -73.9485),
            ("station_008", "Lower East Side - Allen St & Rivington St", 40.7162, -73.9918),
            ("station_009", "Chelsea - 8th Ave & 23rd St", 40.7445, -73.9955),
            ("station_010", "Upper West Side - Central Park West & 72nd St", 40.7755, -73.9762)
        ]
        
        # Insert stations
        for station_id, name, lat, lng in sample_stations:
            cursor.execute("""
                INSERT INTO stations (station_id, name, latitude, longitude)
                VALUES (?, ?, ?, ?)
            """, (station_id, name, lat, lng))
        
        print(f"Created {len(sample_stations)} sample stations")
        
        # Create sample trips
        bike_ids = [f"bike_{i:03d}" for i in range(1, 51)]  # 50 bikes
        trip_count = 0
        
        # Generate trips for the last 30 days
        base_date = datetime.now() - timedelta(days=30)
        
        for day in range(30):
            current_date = base_date + timedelta(days=day)
            
            # Generate 50-200 trips per day
            daily_trips = random.randint(50, 200)
            
            for _ in range(daily_trips):
                # Random bike
                bike_id = random.choice(bike_ids)
                
                # Random start and end stations
                start_station = random.choice(sample_stations)
                end_station = random.choice(sample_stations)
                
                # Random start time (between 6 AM and 10 PM)
                start_hour = random.randint(6, 22)
                start_minute = random.randint(0, 59)
                start_time = current_date.replace(hour=start_hour, minute=start_minute)
                
                # Random trip duration (5-45 minutes)
                duration_minutes = random.randint(5, 45)
                end_time = start_time + timedelta(minutes=duration_minutes)
                
                cursor.execute("""
                    INSERT INTO trips (bike_id, start_station_id, end_station_id, started_at, ended_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (bike_id, start_station[0], end_station[0], start_time, end_time))
                
                trip_count += 1
        
        print(f"Created {trip_count} sample trips")
        
        # Commit changes
        conn.commit()
        
        # Show some statistics
        cursor.execute("SELECT COUNT(*) FROM stations")
        station_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM trips")
        trip_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT bike_id) FROM trips")
        unique_bikes = cursor.fetchone()[0]
        
        print(f"\nDatabase Statistics:")
        print(f"Stations: {station_count}")
        print(f"Trips: {trip_count}")
        print(f"Unique Bikes: {unique_bikes}")
        
        # Show top stations by trip count
        cursor.execute("""
            SELECT s.name, COUNT(t.id) as trip_count
            FROM stations s
            LEFT JOIN trips t ON s.station_id = t.start_station_id
            GROUP BY s.station_id, s.name
            ORDER BY trip_count DESC
            LIMIT 5
        """)
        
        print(f"\nTop 5 stations by trip count:")
        for name, count in cursor.fetchall():
            print(f"  {name}: {count} trips")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    print("Creating sample CitiBike data...")
    create_sample_data()
    print("Sample data creation completed!") 
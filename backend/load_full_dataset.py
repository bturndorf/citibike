#!/usr/bin/env python3
"""
Robust script to load the full CitiBike dataset into Railway PostgreSQL
"""

import os
import sys
import logging
import json
import zipfile
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_tables(engine):
    """Create necessary tables if they don't exist"""
    logger.info("🏗️ Creating tables...")
    
    with engine.connect() as conn:
        # Create stations table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS stations (
                id SERIAL PRIMARY KEY,
                station_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                latitude DECIMAL(10, 8) NOT NULL,
                longitude DECIMAL(11, 8) NOT NULL
            )
        """))
        
        # Create trips table
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
        logger.info("✅ Tables created")

def clear_existing_data(engine):
    """Clear existing data from tables"""
    logger.info("🧹 Clearing existing data...")
    
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM trips"))
        conn.execute(text("DELETE FROM stations"))
        conn.commit()
        logger.info("✅ Existing data cleared")

def load_stations(engine):
    """Load station data"""
    logger.info("🏪 Loading station data...")
    
    stations_file = "../data/citibike_data/stations.json"
    if not os.path.exists(stations_file):
        logger.error(f"❌ Station data file not found: {stations_file}")
        return False
    
    with open(stations_file, 'r') as f:
        stations_data = json.load(f)
    
    stations = stations_data.get('data', {}).get('stations', [])
    logger.info(f"📊 Found {len(stations)} stations")
    
    # Insert stations in batches
    batch_size = 100
    inserted_count = 0
    
    with engine.connect() as conn:
        for i in range(0, len(stations), batch_size):
            batch = stations[i:i+batch_size]
            
            for station in batch:
                try:
                    conn.execute(text("""
                        INSERT INTO stations (station_id, name, latitude, longitude)
                        VALUES (:station_id, :name, :latitude, :longitude)
                    """), {
                        'station_id': station['station_id'],
                        'name': station['name'],
                        'latitude': station['lat'],
                        'longitude': station['lon']
                    })
                    inserted_count += 1
                except Exception as e:
                    logger.warning(f"Skipping duplicate station {station['station_id']}: {e}")
                    continue
            
            conn.commit()
            
            if (i + batch_size) % 500 == 0:
                logger.info(f"✅ Processed {min(i + batch_size, len(stations))} stations...")
    
    logger.info(f"✅ Successfully loaded {inserted_count} stations")
    return True

def load_trips(engine):
    """Load trip data in chunks"""
    logger.info("🚲 Loading trip data...")
    
    trip_file = "../data/citibike_data/202503-citibike-tripdata.csv.zip"
    if not os.path.exists(trip_file):
        logger.error(f"❌ Trip data file not found: {trip_file}")
        return False
    
    # Read the CSV file from zip
    with zipfile.ZipFile(trip_file, 'r') as zip_ref:
        csv_filename = zip_ref.namelist()[0]
        with zip_ref.open(csv_filename) as csv_file:
            # Read in small chunks to handle large file
            chunk_size = 500  # Very small chunks for Railway
            total_trips = 0
            chunk_count = 0
            
            for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
                chunk_count += 1
                
                # Process each chunk in a separate transaction
                with engine.connect() as conn:
                    try:
                        chunk_trips = 0
                        
                        for _, row in chunk.iterrows():
                            try:
                                # Map CitiBike column names to our schema
                                conn.execute(text("""
                                    INSERT INTO trips (bike_id, start_station_id, end_station_id, started_at, ended_at)
                                    VALUES (:bike_id, :start_station_id, :end_station_id, :started_at, :ended_at)
                                """), {
                                    'bike_id': str(row.get('ride_id', 'unknown')),
                                    'start_station_id': str(row.get('start_station_id', '')),
                                    'end_station_id': str(row.get('end_station_id', '')),
                                    'started_at': row.get('started_at', ''),
                                    'ended_at': row.get('ended_at', '')
                                })
                                chunk_trips += 1
                                
                            except Exception as e:
                                logger.warning(f"Skipping invalid trip row: {e}")
                                continue
                        
                        conn.commit()
                        total_trips += chunk_trips
                        
                        # Progress reporting every 10 chunks
                        if chunk_count % 10 == 0:
                            logger.info(f"✅ Processed {total_trips} trips (chunk {chunk_count})...")
                        
                        # Small delay to prevent overwhelming the database
                        time.sleep(0.1)
                        
                    except Exception as e:
                        logger.error(f"Error processing chunk {chunk_count}: {e}")
                        conn.rollback()
                        continue
    
    logger.info(f"✅ Successfully loaded {total_trips} trips")
    return True

def verify_data(engine):
    """Verify the loaded data"""
    logger.info("🔍 Verifying loaded data...")
    
    with engine.connect() as conn:
        station_count = conn.execute(text("SELECT COUNT(*) FROM stations")).scalar()
        trip_count = conn.execute(text("SELECT COUNT(*) FROM trips")).scalar()
        unique_bikes = conn.execute(text("SELECT COUNT(DISTINCT bike_id) FROM trips")).scalar()
    
    logger.info(f"📊 Final database statistics:")
    logger.info(f"  Stations: {station_count}")
    logger.info(f"  Trips: {trip_count}")
    logger.info(f"  Unique Bikes: {unique_bikes}")
    
    return station_count > 0 and trip_count > 0

def main():
    """Main function to load the full dataset"""
    logger.info("🚀 Starting full CitiBike dataset loading...")
    logger.info("=" * 60)
    
    try:
        # Load environment variables
        load_dotenv()
        database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            logger.error("❌ DATABASE_URL environment variable not set")
            return False
        
        logger.info("📊 Connecting to Railway PostgreSQL database...")
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            logger.info("✅ Database connection successful")
        
        # Create tables
        create_tables(engine)
        
        # Clear existing data
        clear_existing_data(engine)
        
        # Load stations
        if not load_stations(engine):
            logger.error("❌ Failed to load stations")
            return False
        
        # Load trips
        if not load_trips(engine):
            logger.error("❌ Failed to load trips")
            return False
        
        # Verify data
        if not verify_data(engine):
            logger.error("❌ Data verification failed")
            return False
        
        logger.info("=" * 60)
        logger.info("✅ Full CitiBike dataset loading complete!")
        logger.info("✅ Application now uses real CitiBike data from Railway PostgreSQL")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error loading full dataset: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 
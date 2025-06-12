#!/usr/bin/env python3
"""
Script to load real CitiBike data into Railway PostgreSQL database
"""

import os
import sys
import logging
import json
import zipfile
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data_to_railway_postgres():
    """Load real CitiBike data into Railway PostgreSQL database"""
    
    logger.info("🔄 Loading real CitiBike data into Railway PostgreSQL database...")
    
    try:
        # Load environment variables
        load_dotenv()
        
        # Get database URL from environment
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            logger.error("❌ DATABASE_URL environment variable not set")
            return False
        
        logger.info(f"📊 Connecting to Railway PostgreSQL database...")
        
        # Create database engine
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            logger.info("✅ Database connection successful")
        
        # Create tables if they don't exist
        with engine.connect() as conn:
            logger.info("🏗️ Creating tables if they don't exist...")
            
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
            logger.info("✅ Tables created successfully")
        
        # Clear existing data
        with engine.connect() as conn:
            logger.info("🧹 Clearing existing data...")
            conn.execute(text("DELETE FROM trips"))
            conn.execute(text("DELETE FROM stations"))
            conn.commit()
            logger.info("✅ Existing data cleared")
        
        # Load station data
        stations_file = "../data/citibike_data/stations.json"
        if os.path.exists(stations_file):
            logger.info("🏪 Loading station data...")
            
            with open(stations_file, 'r') as f:
                stations_data = json.load(f)
            
            stations = stations_data.get('data', {}).get('stations', [])
            logger.info(f"📊 Found {len(stations)} stations")
            
            # Insert stations in a single transaction
            with engine.connect() as conn:
                for station in stations:
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
                    except Exception as e:
                        logger.warning(f"Skipping duplicate station {station['station_id']}: {e}")
                        continue
                
                conn.commit()
            
            logger.info(f"✅ Successfully loaded {len(stations)} stations")
        else:
            logger.error(f"❌ Station data file not found: {stations_file}")
            return False
        
        # Load trip data with better transaction management
        trip_file = "../data/citibike_data/202503-citibike-tripdata.csv.zip"
        if os.path.exists(trip_file):
            logger.info("🚲 Loading trip data...")
            
            # Read the CSV file from zip
            with zipfile.ZipFile(trip_file, 'r') as zip_ref:
                csv_filename = zip_ref.namelist()[0]
                with zip_ref.open(csv_filename) as csv_file:
                    # Read in chunks to handle large file
                    chunk_size = 1000  # Smaller chunks for better transaction management
                    total_trips = 0
                    
                    for chunk_num, chunk in enumerate(pd.read_csv(csv_file, chunksize=chunk_size)):
                        # Use a single connection for each chunk
                        with engine.connect() as conn:
                            try:
                                for _, row in chunk.iterrows():
                                    try:
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
                                        total_trips += 1
                                        
                                    except Exception as e:
                                        logger.warning(f"Skipping invalid trip row: {e}")
                                        continue
                                
                                # Commit the chunk
                                conn.commit()
                                
                            except Exception as e:
                                logger.error(f"Error processing chunk {chunk_num}: {e}")
                                conn.rollback()
                                continue
                        
                        if chunk_num % 10 == 0:
                            logger.info(f"✅ Processed {total_trips} trips...")
            
            logger.info(f"✅ Successfully loaded {total_trips} trips")
        else:
            logger.error(f"❌ Trip data file not found: {trip_file}")
            return False
        
        # Verify data
        with engine.connect() as conn:
            station_count = conn.execute(text("SELECT COUNT(*) FROM stations")).scalar()
            trip_count = conn.execute(text("SELECT COUNT(*) FROM trips")).scalar()
        
        logger.info(f"📊 Final database statistics:")
        logger.info(f"  Stations: {station_count}")
        logger.info(f"  Trips: {trip_count}")
        
        logger.info("✅ Successfully loaded real CitiBike data into Railway PostgreSQL database")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error loading data to Railway PostgreSQL: {e}")
        return False

def main():
    """Main function"""
    logger.info("🚀 Starting Railway PostgreSQL data loading...")
    logger.info("=" * 60)
    
    success = load_data_to_railway_postgres()
    
    if success:
        logger.info("=" * 60)
        logger.info("✅ Railway PostgreSQL data loading complete!")
        logger.info("✅ Application now uses real CitiBike data from Railway PostgreSQL")
    else:
        logger.error("=" * 60)
        logger.error("❌ Railway PostgreSQL data loading failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
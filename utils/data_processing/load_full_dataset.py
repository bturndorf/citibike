#!/usr/bin/env python3
"""
Optimized script to load the full CitiBike dataset into Railway PostgreSQL
Uses bulk inserts and optimized processing for much faster loading
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
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS stations (
                id SERIAL PRIMARY KEY,
                station_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                latitude DECIMAL(10, 8) NOT NULL,
                longitude DECIMAL(11, 8) NOT NULL
            )
        """))
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
    """Load station data using bulk insert"""
    logger.info("🏪 Loading station data...")
    stations_file = "data/citibike_data/stations.json"
    if not os.path.exists(stations_file):
        logger.error(f"❌ Station data file not found: {stations_file}")
        return False
    with open(stations_file, 'r') as f:
        stations_data = json.load(f)
    stations = stations_data.get('data', {}).get('stations', [])
    logger.info(f"📊 Found {len(stations)} stations")
    station_records = []
    for station in stations:
        station_records.append({
            'station_id': station['station_id'],
            'name': station['name'],
            'latitude': station['lat'],
            'longitude': station['lon']
        })
    df_stations = pd.DataFrame(station_records)
    with engine.connect() as conn:
        df_stations.to_sql('stations', conn, if_exists='append', index=False, method='multi')
        conn.commit()
    logger.info(f"✅ Successfully loaded {len(station_records)} stations")
    return True

def load_trips(engine):
    """Load trip data using optimized bulk inserts"""
    logger.info("🚲 Loading trip data...")
    trip_file = "data/citibike_data/202503-citibike-tripdata.csv.zip"
    if not os.path.exists(trip_file):
        logger.error(f"❌ Trip data file not found: {trip_file}")
        return False
    with zipfile.ZipFile(trip_file, 'r') as zip_ref:
        csv_filename = zip_ref.namelist()[0]
        with zip_ref.open(csv_filename) as csv_file:
            chunk_size = 10000  # Increased from 500
            total_trips = 0
            chunk_count = 0
            start_time = time.time()
            for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
                chunk_count += 1
                chunk_start_time = time.time()
                try:
                    chunk_clean = chunk.copy()
                    chunk_clean['bike_id'] = chunk_clean.get('ride_id', 'unknown').astype(str)
                    chunk_clean['start_station_id'] = chunk_clean.get('start_station_id', '').astype(str)
                    chunk_clean['end_station_id'] = chunk_clean.get('end_station_id', '').astype(str)
                    chunk_clean['started_at'] = pd.to_datetime(chunk_clean.get('started_at', ''), errors='coerce')
                    chunk_clean['ended_at'] = pd.to_datetime(chunk_clean.get('ended_at', ''), errors='coerce')
                    chunk_clean = chunk_clean.dropna(subset=['started_at', 'ended_at'])
                    if len(chunk_clean) == 0:
                        continue
                    chunk_clean = chunk_clean[['bike_id', 'start_station_id', 'end_station_id', 'started_at', 'ended_at']]
                    with engine.connect() as conn:
                        chunk_clean.to_sql('trips', conn, if_exists='append', index=False, method='multi')
                        conn.commit()
                    chunk_trips = len(chunk_clean)
                    total_trips += chunk_trips
                    chunk_time = time.time() - chunk_start_time
                    if chunk_count % 5 == 0:
                        elapsed_time = time.time() - start_time
                        trips_per_second = total_trips / elapsed_time if elapsed_time > 0 else 0
                        logger.info(f"✅ Processed {total_trips:,} trips (chunk {chunk_count}) - "
                                    f"{chunk_trips:,} in {chunk_time:.1f}s - "
                                    f"Rate: {trips_per_second:.0f} trips/sec")
                except Exception as e:
                    logger.error(f"Error processing chunk {chunk_count}: {e}")
                    continue
    total_time = time.time() - start_time
    avg_rate = total_trips / total_time if total_time > 0 else 0
    logger.info(f"✅ Successfully loaded {total_trips:,} trips in {total_time:.1f}s")
    logger.info(f"📊 Average rate: {avg_rate:.0f} trips/second")
    return True

def verify_data(engine):
    """Verify the loaded data"""
    logger.info("🔍 Verifying loaded data...")
    with engine.connect() as conn:
        station_count = conn.execute(text("SELECT COUNT(*) FROM stations")).scalar()
        trip_count = conn.execute(text("SELECT COUNT(*) FROM trips")).scalar()
        unique_bikes = conn.execute(text("SELECT COUNT(DISTINCT bike_id) FROM trips")).scalar()
    logger.info(f"📊 Final database statistics:")
    logger.info(f"  Stations: {station_count:,}")
    logger.info(f"  Trips: {trip_count:,}")
    logger.info(f"  Unique Bikes: {unique_bikes:,}")
    return station_count > 0 and trip_count > 0

def main():
    """Main function to load the full dataset"""
    logger.info("🚀 Starting optimized CitiBike dataset loading...")
    logger.info("=" * 60)
    try:
        load_dotenv()
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            logger.error("❌ DATABASE_URL environment variable not set")
            return False
        logger.info("📊 Connecting to Railway PostgreSQL database...")
        engine = create_engine(database_url)
        with engine.connect() as conn:
            logger.info("✅ Database connection successful")
        create_tables(engine)
        clear_existing_data(engine)
        if not load_stations(engine):
            logger.error("❌ Failed to load stations")
            return False
        if not load_trips(engine):
            logger.error("❌ Failed to load trips")
            return False
        if not verify_data(engine):
            logger.error("❌ Data verification failed")
            return False
        logger.info("=" * 60)
        logger.info("✅ Optimized CitiBike dataset loading complete!")
        logger.info("✅ Application now uses real CitiBike data from Railway PostgreSQL")
        return True
    except Exception as e:
        logger.error(f"❌ Error loading full dataset: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 
#!/usr/bin/env python3
"""
Script to load only station data into Railway PostgreSQL database
"""

import os
import sys
import logging
import json
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_stations_to_railway_postgres():
    """Load only station data into Railway PostgreSQL database"""
    
    logger.info("🔄 Loading station data into Railway PostgreSQL database...")
    
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
        
        # Create stations table if it doesn't exist
        with engine.connect() as conn:
            logger.info("🏗️ Creating stations table if it doesn't exist...")
            
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS stations (
                    id SERIAL PRIMARY KEY,
                    station_id VARCHAR(50) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    latitude DECIMAL(10, 8) NOT NULL,
                    longitude DECIMAL(11, 8) NOT NULL
                )
            """))
            
            conn.commit()
            logger.info("✅ Stations table created successfully")
        
        # Clear existing station data
        with engine.connect() as conn:
            logger.info("🧹 Clearing existing station data...")
            conn.execute(text("DELETE FROM stations"))
            conn.commit()
            logger.info("✅ Existing station data cleared")
        
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
                inserted_count = 0
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
                        inserted_count += 1
                    except Exception as e:
                        logger.warning(f"Skipping duplicate station {station['station_id']}: {e}")
                        continue
                
                conn.commit()
            
            logger.info(f"✅ Successfully loaded {inserted_count} stations")
        else:
            logger.error(f"❌ Station data file not found: {stations_file}")
            return False
        
        # Verify data
        with engine.connect() as conn:
            station_count = conn.execute(text("SELECT COUNT(*) FROM stations")).scalar()
        
        logger.info(f"📊 Final database statistics:")
        logger.info(f"  Stations: {station_count}")
        
        logger.info("✅ Successfully loaded station data into Railway PostgreSQL database")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error loading station data to Railway PostgreSQL: {e}")
        return False

def main():
    """Main function"""
    logger.info("🚀 Starting Railway PostgreSQL station data loading...")
    logger.info("=" * 60)
    
    success = load_stations_to_railway_postgres()
    
    if success:
        logger.info("=" * 60)
        logger.info("✅ Railway PostgreSQL station data loading complete!")
        logger.info("✅ Application now has real station data from Railway PostgreSQL")
    else:
        logger.error("=" * 60)
        logger.error("❌ Railway PostgreSQL station data loading failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
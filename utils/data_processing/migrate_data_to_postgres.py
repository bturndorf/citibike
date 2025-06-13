#!/usr/bin/env python3
"""
Data Migration Script: SQLite to PostgreSQL

This script migrates data from the existing SQLite database to the new PostgreSQL database.
"""

import os
import sys
import logging
import json
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def migrate_data_from_sqlite():
    """Migrate data from SQLite to PostgreSQL using fast bulk operations"""
    logger.info("🔄 Migrating data from SQLite to PostgreSQL...")
    
    try:
        # Connect to SQLite database
        sqlite_url = "sqlite:///./dev.db"
        sqlite_engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
        
        # Connect to PostgreSQL database
        load_dotenv()
        postgres_url = os.getenv("DATABASE_URL")
        if not postgres_url:
            logger.error("❌ DATABASE_URL not set in environment")
            return False
            
        postgres_engine = create_engine(postgres_url)
        
        # Clear existing data in PostgreSQL
        with postgres_engine.connect() as conn:
            conn.execute(text("DELETE FROM trips"))
            conn.execute(text("DELETE FROM stations"))
            conn.execute(text("DELETE FROM station_mapping"))
            conn.commit()
            logger.info("🧹 Cleared existing PostgreSQL data")
        
        # Migrate stations using pandas bulk insert
        logger.info("📊 Migrating stations...")
        stations_df = pd.read_sql("SELECT station_id, name, latitude, longitude FROM stations", sqlite_engine)
        if not stations_df.empty:
            stations_df.to_sql('stations', postgres_engine, if_exists='append', index=False, method='multi')
            logger.info(f"✅ Migrated {len(stations_df)} stations")
        
        # Migrate trips using pandas bulk insert with chunking
        logger.info("🚲 Migrating trips...")
        trip_count = pd.read_sql("SELECT COUNT(*) as count FROM trips", sqlite_engine).iloc[0]['count']
        logger.info(f"🔄 Migrating {trip_count:,} trips...")
        
        # Use larger chunks for better performance
        chunk_size = 50000
        total_migrated = 0
        
        for chunk_num, chunk_df in enumerate(pd.read_sql("SELECT bike_id, start_station_id, end_station_id, started_at, ended_at FROM trips", sqlite_engine, chunksize=chunk_size)):
            chunk_df.to_sql('trips', postgres_engine, if_exists='append', index=False, method='multi')
            total_migrated += len(chunk_df)
            logger.info(f"   Migrated {total_migrated:,} trips...")
        
        logger.info(f"✅ Migrated {total_migrated:,} trips total")
        
        # Create station mapping (if stations.json exists)
        stations_json_path = "../data/citibike_data/stations.json"
        if os.path.exists(stations_json_path):
            logger.info("🗺️ Creating station mapping...")
            with open(stations_json_path, 'r') as f:
                stations_data = json.load(f)
            
            # Convert to DataFrame for bulk insert
            mapping_data = []
            for station in stations_data:
                # Handle both dict and string formats
                if isinstance(station, dict):
                    mapping_data.append({
                        'uuid_station_id': station['station_id'],
                        'numeric_station_id': station['station_id'],  # This will be updated with actual mapping
                        'station_name': station['name']
                    })
                else:
                    # If station is a string, skip it
                    logger.warning(f"Skipping non-dict station data: {station}")
                    continue
            
            if mapping_data:
                mapping_df = pd.DataFrame(mapping_data)
                mapping_df.to_sql('station_mapping', postgres_engine, if_exists='append', index=False, method='multi')
                logger.info(f"✅ Created station mapping for {len(mapping_data)} stations")
            else:
                logger.warning("⚠️ No valid station mapping data found")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error migrating data: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def verify_migration(engine):
    """Verify the migration was successful"""
    logger.info("🔍 Verifying migration...")
    
    try:
        with engine.connect() as conn:
            # Check station count
            station_count = conn.execute(text("SELECT COUNT(*) FROM stations")).scalar()
            logger.info(f"📊 Stations: {station_count:,}")
            
            # Check trip count
            trip_count = conn.execute(text("SELECT COUNT(*) FROM trips")).scalar()
            logger.info(f"🚲 Trips: {trip_count:,}")
            
            # Check mapping count
            mapping_count = conn.execute(text("SELECT COUNT(*) FROM station_mapping")).scalar()
            logger.info(f"🗺️ Station mappings: {mapping_count:,}")
            
            # Check date range
            date_result = conn.execute(text("""
                SELECT MIN(started_at), MAX(started_at) 
                FROM trips 
                WHERE started_at IS NOT NULL
            """)).fetchone()
            
            if date_result and date_result[0]:
                logger.info(f"📅 Date range: {date_result[0]} to {date_result[1]}")
            
            logger.info("✅ Migration verification complete")
            return True
            
    except Exception as e:
        logger.error(f"❌ Error verifying migration: {e}")
        return False

def main():
    """Main migration function"""
    logger.info("🚀 Starting data migration from SQLite to PostgreSQL...")
    logger.info("=" * 60)
    
    # Check if SQLite database exists
    sqlite_db_path = "./dev.db"
    if not os.path.exists(sqlite_db_path):
        logger.error(f"❌ SQLite database not found: {sqlite_db_path}")
        logger.info("💡 Make sure you have the SQLite database file in the backend directory")
        return False
    
    # Load environment variables
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        logger.error("❌ DATABASE_URL not set in environment")
        logger.info("💡 Please set DATABASE_URL in your .env file")
        logger.info("💡 Example: DATABASE_URL=postgresql://Ben@localhost:5432/dev")
        return False
    
    # Test PostgreSQL connection
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            logger.info("✅ PostgreSQL connection successful")
    except Exception as e:
        logger.error(f"❌ PostgreSQL connection failed: {e}")
        return False
    
    # Migrate data
    if not migrate_data_from_sqlite():
        logger.error("❌ Data migration failed")
        return False
    
    # Verify migration
    if not verify_migration(engine):
        logger.error("❌ Migration verification failed")
        return False
    
    logger.info("=" * 60)
    logger.info("✅ Data migration completed successfully!")
    logger.info("💡 Your application now uses PostgreSQL with migrated data")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
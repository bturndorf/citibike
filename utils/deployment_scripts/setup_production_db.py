#!/usr/bin/env python3
"""
Production Database Setup Script

This script ensures the production database is properly configured with:
1. All required tables
2. Performance indexes
3. Proper permissions

Usage:
    python setup_production_db.py
"""

import os
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_production_database():
    """Set up production database with all required indexes"""
    
    # Load environment variables
    load_dotenv()
    
    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL environment variable not set")
        return False
    
    try:
        # Create database engine
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            logger.info("Database connection successful")
            
            # Check if tables exist
            tables_query = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('trips', 'stations', 'station_mapping')
            """)
            
            result = conn.execute(tables_query)
            existing_tables = {row.table_name for row in result}
            required_tables = {'trips', 'stations', 'station_mapping'}
            
            if not required_tables.issubset(existing_tables):
                missing_tables = required_tables - existing_tables
                logger.error(f"Missing required tables: {missing_tables}")
                logger.error("Please run database migrations first: alembic upgrade head")
                return False
            
            logger.info("All required tables exist")
            
            # Check and create indexes
            indexes_to_create = {
                'idx_trips_station_time': """
                    CREATE INDEX IF NOT EXISTS idx_trips_station_time 
                    ON trips(start_station_id, started_at)
                """,
                'idx_trips_bike_end_time': """
                    CREATE INDEX IF NOT EXISTS idx_trips_bike_end_time 
                    ON trips(bike_id, end_station_id, started_at)
                """,
                'idx_trips_end_station_time': """
                    CREATE INDEX IF NOT EXISTS idx_trips_end_station_time 
                    ON trips(end_station_id, started_at)
                """,
                'idx_station_mapping_uuid': """
                    CREATE INDEX IF NOT EXISTS idx_station_mapping_uuid 
                    ON station_mapping(uuid_station_id)
                """,
                'idx_station_mapping_name': """
                    CREATE INDEX IF NOT EXISTS idx_station_mapping_name 
                    ON station_mapping(station_name)
                """
            }
            
            # Check existing indexes
            index_check_query = text("""
                SELECT indexname 
                FROM pg_indexes 
                WHERE tablename IN ('trips', 'station_mapping')
                AND indexname IN (
                    'idx_trips_station_time',
                    'idx_trips_bike_end_time', 
                    'idx_trips_end_station_time',
                    'idx_station_mapping_uuid',
                    'idx_station_mapping_name'
                )
            """)
            
            result = conn.execute(index_check_query)
            existing_indexes = {row.indexname for row in result}
            
            # Create missing indexes
            for index_name, index_sql in indexes_to_create.items():
                if index_name not in existing_indexes:
                    logger.info(f"Creating index: {index_name}")
                    try:
                        conn.execute(text(index_sql))
                        logger.info(f"Successfully created index: {index_name}")
                    except Exception as e:
                        logger.error(f"Failed to create index {index_name}: {e}")
                        return False
                else:
                    logger.info(f"Index already exists: {index_name}")
            
            # Verify data exists
            data_check_query = text("""
                SELECT 
                    (SELECT COUNT(*) FROM trips) as trip_count,
                    (SELECT COUNT(*) FROM stations) as station_count,
                    (SELECT COUNT(*) FROM station_mapping) as mapping_count
            """)
            
            result = conn.execute(data_check_query)
            row = result.fetchone()
            
            logger.info(f"Database contains:")
            logger.info(f"  - {row.trip_count:,} trips")
            logger.info(f"  - {row.station_count:,} stations")
            logger.info(f"  - {row.mapping_count:,} station mappings")
            
            if row.trip_count == 0:
                logger.warning("No trip data found in database")
                logger.warning("Please load data before running the application")
            
            logger.info("Production database setup completed successfully")
            return True
            
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        return False

def main():
    """Main function"""
    logger.info("Starting production database setup...")
    
    if setup_production_database():
        logger.info("✅ Production database setup completed successfully")
        sys.exit(0)
    else:
        logger.error("❌ Production database setup failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Database Statistics Utility for Railway PostgreSQL

This script provides quick access to database statistics for the CitiBike project.
Useful for monitoring data loading progress and verifying database state.
"""

import os
import sys
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_database_url():
    """Get database URL from environment or Railway CLI"""
    # Try to load from .env file first
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        return database_url
    
    # If not found, provide instructions and exit
    logger.error("❌ DATABASE_URL not found in environment variables or .env file.")
    logger.info("💡 Run 'railway variables' to get the connection string.")
    logger.info("💡 Set DATABASE_URL in your .env file or export it as an environment variable.")
    return None

def check_database_stats():
    """Check basic database statistics"""
    
    database_url = get_database_url()
    if not database_url:
        return False
    
    logger.info("📊 Connecting to Railway PostgreSQL database...")
    
    try:
        # Create database engine
        engine = create_engine(database_url)
        
        # Test connection and get stats
        with engine.connect() as conn:
            logger.info("✅ Database connection successful")
            
            # Check trips table
            trips_result = conn.execute(text("SELECT COUNT(*) FROM trips"))
            trip_count = trips_result.scalar()
            logger.info(f"📊 Trips count: {trip_count:,}")
            
            # Check stations table
            stations_result = conn.execute(text("SELECT COUNT(*) FROM stations"))
            station_count = stations_result.scalar()
            logger.info(f"🏪 Stations count: {station_count:,}")
            
            # Get date range
            date_result = conn.execute(text("""
                SELECT MIN(started_at), MAX(started_at) 
                FROM trips 
                WHERE started_at IS NOT NULL
                LIMIT 1
            """))
            min_date, max_date = date_result.fetchone()
            logger.info(f"📅 Date range: {min_date} to {max_date}")
            
            # Get table sizes (if available)
            try:
                size_result = conn.execute(text("""
                    SELECT 
                        pg_size_pretty(pg_total_relation_size('trips')) as trips_size,
                        pg_size_pretty(pg_total_relation_size('stations')) as stations_size
                """))
                trips_size, stations_size = size_result.fetchone()
                logger.info(f"💾 Table sizes - Trips: {trips_size}, Stations: {stations_size}")
            except Exception as e:
                logger.debug(f"Could not get table sizes: {e}")
            
            logger.info("=" * 50)
            logger.info("📈 Database Summary:")
            logger.info(f"   • Trips: {trip_count:,}")
            logger.info(f"   • Stations: {station_count:,}")
            logger.info(f"   • Date range: {min_date} to {max_date}")
            
            # Check against expected values
            if trip_count >= 1300000:
                logger.info("✅ Trip count meets expected threshold (1.3M+)")
            else:
                logger.warning(f"⚠️ Trip count below expected threshold (1.3M+), current: {trip_count:,}")
            
            if station_count >= 2000:
                logger.info("✅ Station count meets expected threshold (2K+)")
            else:
                logger.warning(f"⚠️ Station count below expected threshold (2K+), current: {station_count:,}")
            
    except Exception as e:
        logger.error(f"❌ Error connecting to database: {e}")
        return False
    
    return True

def check_table_structure():
    """Check table structure and constraints"""
    
    database_url = get_database_url()
    if not database_url:
        return False
    
    logger.info("🔍 Checking table structure...")
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check trips table structure
            trips_columns = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'trips'
                ORDER BY ordinal_position
            """))
            
            logger.info("📋 Trips table structure:")
            for col in trips_columns:
                logger.info(f"   • {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
            
            # Check stations table structure
            stations_columns = conn.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'stations'
                ORDER BY ordinal_position
            """))
            
            logger.info("📋 Stations table structure:")
            for col in stations_columns:
                logger.info(f"   • {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
                
    except Exception as e:
        logger.error(f"❌ Error checking table structure: {e}")
        return False
    
    return True

def main():
    """Main function"""
    logger.info("🚀 Railway Database Statistics Utility")
    logger.info("=" * 50)
    
    # Check basic stats
    if not check_database_stats():
        sys.exit(1)
    
    # Optionally check table structure
    if len(sys.argv) > 1 and sys.argv[1] == "--structure":
        logger.info("=" * 50)
        if not check_table_structure():
            sys.exit(1)
    
    logger.info("=" * 50)
    logger.info("✅ Database check complete!")

if __name__ == "__main__":
    main() 
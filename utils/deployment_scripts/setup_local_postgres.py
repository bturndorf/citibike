#!/usr/bin/env python3
"""
Local PostgreSQL Setup Script for CitiBike Development

This script sets up a local PostgreSQL database for development,
replacing the SQLite database to match the production Railway environment.
"""

import os
import sys
import logging
import subprocess
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_postgres_installation():
    """Check if PostgreSQL is installed and running"""
    try:
        # Check if psql is available
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ PostgreSQL found: {result.stdout.strip()}")
            return True
        else:
            logger.error("❌ PostgreSQL not found in PATH")
            return False
    except FileNotFoundError:
        logger.error("❌ PostgreSQL not installed or not in PATH")
        return False

def create_local_database():
    """Create local PostgreSQL database for development"""
    try:
        # Create database using psql
        db_name = "dev"
        
        # Try to create database
        create_cmd = f"createdb {db_name}"
        logger.info(f"Creating database: {db_name}")
        
        result = subprocess.run(create_cmd.split(), capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"✅ Database '{db_name}' created successfully")
            return True
        elif "already exists" in result.stderr:
            logger.info(f"✅ Database '{db_name}' already exists")
            return True
        else:
            logger.error(f"❌ Failed to create database: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error creating database: {e}")
        return False

def create_tables(engine):
    """Create necessary tables in PostgreSQL"""
    logger.info("🏗️ Creating tables in PostgreSQL...")
    
    try:
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
            
            # Create station_mapping table (for UUID to numeric ID mapping)
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS station_mapping (
                    uuid_station_id VARCHAR(50) PRIMARY KEY,
                    numeric_station_id VARCHAR(50) NOT NULL,
                    station_name VARCHAR(255) NOT NULL
                )
            """))
            
            # Create indexes for performance
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_trips_bike_id ON trips(bike_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_trips_stations ON trips(start_station_id, end_station_id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_trips_time ON trips(started_at)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_station_mapping_numeric ON station_mapping(numeric_station_id)"))
            
            conn.commit()
            logger.info("✅ Tables and indexes created successfully")
            return True
            
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")
        return False

def main():
    """Main migration function"""
    logger.info("🚀 Starting local PostgreSQL setup...")
    logger.info("=" * 60)
    
    # Step 1: Check PostgreSQL installation
    if not check_postgres_installation():
        logger.error("❌ PostgreSQL not available. Please install PostgreSQL first.")
        logger.info("💡 Installation instructions:")
        logger.info("   macOS: brew install postgresql")
        logger.info("   Ubuntu: sudo apt-get install postgresql postgresql-contrib")
        logger.info("   Windows: Download from https://www.postgresql.org/download/windows/")
        return False
    
    # Step 2: Create local database
    if not create_local_database():
        logger.error("❌ Failed to create local database")
        return False
    
    # Step 3: Set up environment
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        # Create local PostgreSQL URL using current user
        import getpass
        current_user = getpass.getuser()
        local_url = f"postgresql://{current_user}@localhost:5432/dev"
        logger.info(f"💡 Setting DATABASE_URL to: {local_url}")
        logger.info("💡 Add this to your .env file:")
        logger.info(f"   DATABASE_URL={local_url}")
        
        # Set environment variable for this session
        os.environ["DATABASE_URL"] = local_url
        database_url = local_url
    
    # Step 4: Create tables
    engine = create_engine(database_url)
    if not create_tables(engine):
        logger.error("❌ Failed to create tables")
        return False
    
    logger.info("=" * 60)
    logger.info("✅ Local PostgreSQL setup completed successfully!")
    logger.info("💡 Next steps:")
    logger.info("   1. Update your .env file with the local DATABASE_URL")
    logger.info("   2. Run data migration script if needed")
    logger.info("   3. Test the application with: python main.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
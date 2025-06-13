#!/usr/bin/env python3
"""
Script to load real CitiBike data into the database and verify data sources
"""

import os
import sys
import sqlite3
import logging
from data_ingestion import CitiBikeDataIngestion

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def verify_data_sources():
    """Verify that the application is using real CitiBike data"""
    
    logger.info("🔍 Verifying data sources...")
    
    # Check if real data files exist
    data_dir = "../data/citibike_data"
    stations_file = os.path.join(data_dir, "stations.json")
    trip_file = os.path.join(data_dir, "202503-citibike-tripdata.csv.zip")
    
    logger.info(f"Checking for real data files:")
    logger.info(f"  Stations file: {stations_file} - {'✅ EXISTS' if os.path.exists(stations_file) else '❌ MISSING'}")
    logger.info(f"  Trip data file: {trip_file} - {'✅ EXISTS' if os.path.exists(trip_file) else '❌ MISSING'}")
    
    # Check database content
    db_path = "dev.db"
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check station count
        cursor.execute("SELECT COUNT(*) FROM stations")
        station_count = cursor.fetchone()[0]
        
        # Check trip count
        cursor.execute("SELECT COUNT(*) FROM trips")
        trip_count = cursor.fetchone()[0]
        
        # Check unique bikes
        cursor.execute("SELECT COUNT(DISTINCT bike_id) FROM trips")
        unique_bikes = cursor.fetchone()[0]
        
        # Check sample station names
        cursor.execute("SELECT name FROM stations LIMIT 3")
        sample_stations = [row[0] for row in cursor.fetchall()]
        
        # Check sample bike IDs
        cursor.execute("SELECT DISTINCT bike_id FROM trips LIMIT 5")
        sample_bikes = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        logger.info(f"\n📊 Database Statistics:")
        logger.info(f"  Stations: {station_count}")
        logger.info(f"  Trips: {trip_count}")
        logger.info(f"  Unique Bikes: {unique_bikes}")
        
        logger.info(f"\n🏪 Sample Stations:")
        for station in sample_stations:
            logger.info(f"  - {station}")
        
        logger.info(f"\n🚲 Sample Bike IDs:")
        for bike in sample_bikes:
            logger.info(f"  - {bike}")
        
        # Determine if using real or sample data
        if station_count > 100 and trip_count > 100000:
            logger.info(f"\n✅ REAL DATA DETECTED")
            logger.info(f"  - Large number of stations ({station_count}) indicates real CitiBike data")
            logger.info(f"  - Large number of trips ({trip_count}) indicates real trip data")
            return True
        else:
            logger.info(f"\n❌ SAMPLE DATA DETECTED")
            logger.info(f"  - Small number of stations ({station_count}) indicates sample data")
            logger.info(f"  - Small number of trips ({trip_count}) indicates sample data")
            return False
    else:
        logger.error(f"❌ Database file {db_path} not found")
        return False

def load_real_data():
    """Load real CitiBike data into the database"""
    
    logger.info("🔄 Loading real CitiBike data into database...")
    
    try:
        # Initialize data ingestion
        ingestion = CitiBikeDataIngestion()
        
        # Load real data into database
        success = ingestion.load_real_data_to_database()
        
        if success:
            logger.info("✅ Successfully loaded real CitiBike data")
            return True
        else:
            logger.error("❌ Failed to load real CitiBike data")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error loading real data: {e}")
        return False

def main():
    """Main function to verify and load real data"""
    
    logger.info("🚀 Starting CitiBike Data Source Verification")
    logger.info("=" * 50)
    
    # First, verify current data sources
    using_real_data = verify_data_sources()
    
    if not using_real_data:
        logger.info("\n🔄 Loading real CitiBike data...")
        success = load_real_data()
        
        if success:
            logger.info("\n🔍 Re-verifying data sources after loading...")
            verify_data_sources()
        else:
            logger.error("\n❌ Failed to load real data. Application will continue using sample data.")
            sys.exit(1)
    else:
        logger.info("\n✅ Application is already using real CitiBike data!")
    
    logger.info("\n" + "=" * 50)
    logger.info("✅ Data Source Verification Complete")
    logger.info("✅ Application now uses real CitiBike data for calculations")

if __name__ == "__main__":
    main() 
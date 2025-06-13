#!/usr/bin/env python3
"""
Script to populate the station_mapping table with data from stations.json
This maps UUID station IDs to numeric IDs and station names for the probability calculations.
"""

import json
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql:///dev")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def populate_station_mapping():
    """Populate the station_mapping table with data from stations.json"""
    
    # Path to stations.json
    stations_file = "../data/citibike_data/stations.json"
    
    if not os.path.exists(stations_file):
        logger.error(f"Stations file not found: {stations_file}")
        return False
    
    try:
        # Load stations data
        logger.info(f"Loading stations data from {stations_file}")
        with open(stations_file, 'r') as f:
            data = json.load(f)
        
        stations = data.get('data', {}).get('stations', [])
        logger.info(f"Found {len(stations)} stations in JSON file")
        
        # Create database session
        db = SessionLocal()
        
        # Clear existing mapping data
        logger.info("Clearing existing station mapping data")
        db.execute(text("DELETE FROM station_mapping"))
        db.commit()
        
        # Prepare mapping data
        mapping_data = []
        for station in stations:
            station_id = station.get('station_id')
            short_name = station.get('short_name')
            name = station.get('name')
            
            if station_id and short_name and name:
                mapping_data.append({
                    'uuid_station_id': station_id,
                    'numeric_station_id': short_name,
                    'station_name': name
                })
        
        logger.info(f"Prepared {len(mapping_data)} station mappings")
        
        # Insert mapping data in batches
        batch_size = 1000
        for i in range(0, len(mapping_data), batch_size):
            batch = mapping_data[i:i + batch_size]
            
            # Create values string for bulk insert
            values = []
            for item in batch:
                # Escape single quotes in station names
                escaped_name = item['station_name'].replace("'", "''")
                values.append(f"('{item['uuid_station_id']}', '{item['numeric_station_id']}', '{escaped_name}')")
            
            values_str = ', '.join(values)
            
            # Execute bulk insert
            insert_query = text(f"""
                INSERT INTO station_mapping (uuid_station_id, numeric_station_id, station_name)
                VALUES {values_str}
                ON CONFLICT (uuid_station_id) DO UPDATE SET
                    numeric_station_id = EXCLUDED.numeric_station_id,
                    station_name = EXCLUDED.station_name
            """)
            
            db.execute(insert_query)
            logger.info(f"Inserted batch {i//batch_size + 1}/{(len(mapping_data) + batch_size - 1)//batch_size}")
        
        # Commit all changes
        db.commit()
        
        # Verify the data was inserted
        result = db.execute(text("SELECT COUNT(*) FROM station_mapping"))
        count = result.scalar()
        logger.info(f"Successfully populated station_mapping table with {count} records")
        
        # Show some sample mappings
        result = db.execute(text("SELECT * FROM station_mapping LIMIT 5"))
        sample_mappings = result.fetchall()
        logger.info("Sample mappings:")
        for mapping in sample_mappings:
            logger.info(f"  UUID: {mapping[0]}, Numeric: {mapping[1]}, Name: {mapping[2]}")
        
        db.close()
        return True
        
    except Exception as e:
        logger.error(f"Error populating station mapping: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def verify_mapping():
    """Verify that the mapping table works correctly with the trips table"""
    try:
        db = SessionLocal()
        
        # Test a join query
        query = text("""
            SELECT 
                sm.station_name,
                sm.uuid_station_id,
                sm.numeric_station_id,
                COUNT(t.id) as trip_count
            FROM station_mapping sm
            LEFT JOIN trips t ON sm.numeric_station_id = t.start_station_id
            GROUP BY sm.station_name, sm.uuid_station_id, sm.numeric_station_id
            ORDER BY trip_count DESC
            LIMIT 10
        """)
        
        result = db.execute(query)
        mappings = result.fetchall()
        
        logger.info("Top 10 stations by trip count (using mapping):")
        for mapping in mappings:
            logger.info(f"  {mapping[0]} (UUID: {mapping[1]}, Numeric: {mapping[2]}) - {mapping[3]} trips")
        
        db.close()
        return True
        
    except Exception as e:
        logger.error(f"Error verifying mapping: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting station mapping population...")
    
    if populate_station_mapping():
        logger.info("Station mapping population completed successfully")
        
        logger.info("Verifying mapping...")
        if verify_mapping():
            logger.info("Mapping verification completed successfully")
        else:
            logger.error("Mapping verification failed")
    else:
        logger.error("Station mapping population failed")
        sys.exit(1) 
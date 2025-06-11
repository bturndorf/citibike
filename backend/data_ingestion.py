#!/usr/bin/env python3
"""
CitiBike Data Ingestion Script
Downloads and analyzes CitiBike trip data for the MVP
"""

import requests
import pandas as pd
import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import zipfile
import io
import sqlite3
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CitiBikeDataIngestion:
    def __init__(self, data_dir: str = "../data/citibike_data"):
        self.data_dir = data_dir
        self.base_url = "https://s3.amazonaws.com/tripdata"
        self.stations_url = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
    
    def download_trip_data(self, months: int = 3) -> List[str]:
        """
        Download CitiBike trip data for the specified number of months (historical)
        Returns list of downloaded file paths
        """
        downloaded_files = []
        current_date = datetime.now()
        
        # Start from 3 months ago and go backwards
        for i in range(months):
            # Calculate date for each month (going backwards)
            target_date = current_date - timedelta(days=30*(i+1))
            year = target_date.year
            month = target_date.month
            
            # Format filename (e.g., 202312-citibike-tripdata.csv.zip)
            filename = f"{year}{month:02d}-citibike-tripdata.csv.zip"
            url = f"{self.base_url}/{filename}"
            local_path = os.path.join(self.data_dir, filename)
            
            try:
                logger.info(f"Downloading {filename}...")
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                # Save the file
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                
                downloaded_files.append(local_path)
                logger.info(f"Successfully downloaded {filename}")
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Failed to download {filename}: {e}")
                continue
        
        return downloaded_files
    
    def download_station_data(self) -> str:
        """
        Download current station information
        Returns path to downloaded file
        """
        try:
            logger.info("Downloading station information...")
            response = requests.get(self.stations_url, timeout=30)
            response.raise_for_status()
            
            station_data = response.json()
            local_path = os.path.join(self.data_dir, "stations.json")
            
            with open(local_path, 'w') as f:
                import json
                json.dump(station_data, f, indent=2)
            
            logger.info("Successfully downloaded station information")
            return local_path
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download station data: {e}")
            return None
    
    def analyze_trip_data(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a single trip data file
        Returns analysis results
        """
        try:
            # Read the CSV file from zip
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                csv_filename = zip_ref.namelist()[0]  # Get the first file in zip
                with zip_ref.open(csv_filename) as csv_file:
                    df = pd.read_csv(csv_file)
            
            analysis = {
                'file': file_path,
                'rows': len(df),
                'columns': list(df.columns),
                'missing_data': df.isnull().sum().to_dict(),
                'data_types': df.dtypes.to_dict(),
                'sample_data': df.head(3).to_dict('records')
            }
            
            # Check for required columns
            required_columns = ['bikeid', 'start station id', 'end station id', 'starttime', 'stoptime']
            missing_columns = [col for col in required_columns if col not in df.columns]
            analysis['missing_required_columns'] = missing_columns
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return {'file': file_path, 'error': str(e)}
    
    def analyze_station_data(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze station data
        Returns analysis results
        """
        try:
            with open(file_path, 'r') as f:
                import json
                data = json.load(f)
            
            stations = data.get('data', {}).get('stations', [])
            
            analysis = {
                'file': file_path,
                'total_stations': len(stations),
                'sample_stations': stations[:3] if stations else []
            }
            
            if stations:
                # Check for required fields
                required_fields = ['station_id', 'name', 'lat', 'lon']
                sample_station = stations[0]
                missing_fields = [field for field in required_fields if field not in sample_station]
                analysis['missing_required_fields'] = missing_fields
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing station data {file_path}: {e}")
            return {'file': file_path, 'error': str(e)}
    
    def generate_quality_report(self, trip_files: List[str], station_file: str) -> Dict[str, Any]:
        """
        Generate a comprehensive data quality report
        """
        logger.info("Generating data quality report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'trip_data_analysis': [],
            'station_data_analysis': None,
            'summary': {}
        }
        
        # Analyze trip data
        for file_path in trip_files:
            analysis = self.analyze_trip_data(file_path)
            report['trip_data_analysis'].append(analysis)
        
        # Analyze station data
        if station_file:
            report['station_data_analysis'] = self.analyze_station_data(station_file)
        
        # Generate summary
        total_trips = sum(analysis.get('rows', 0) for analysis in report['trip_data_analysis'])
        report['summary'] = {
            'total_trip_files': len(trip_files),
            'total_trips': total_trips,
            'has_station_data': station_file is not None
        }
        
        return report

    def load_real_data_to_database(self, db_path: str = "dev.db") -> bool:
        """
        Load real CitiBike data into the SQLite database
        Returns True if successful, False otherwise
        """
        try:
            logger.info("Loading real CitiBike data into database...")
            
            # Connect to database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Clear existing data
            cursor.execute("DELETE FROM trips")
            cursor.execute("DELETE FROM stations")
            
            # Reset auto-increment counters (SQLite specific)
            try:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('stations', 'trips')")
            except sqlite3.OperationalError:
                # sqlite_sequence table doesn't exist, which is fine
                pass
            
            # Load real station data
            stations_file = os.path.join(self.data_dir, "stations.json")
            if os.path.exists(stations_file):
                logger.info("Loading real station data...")
                with open(stations_file, 'r') as f:
                    stations_data = json.load(f)
                
                stations = stations_data.get('data', {}).get('stations', [])
                logger.info(f"Found {len(stations)} real stations")
                
                # Insert real stations
                for station in stations:
                    cursor.execute("""
                        INSERT INTO stations (station_id, name, latitude, longitude)
                        VALUES (?, ?, ?, ?)
                    """, (
                        station['station_id'],
                        station['name'],
                        station['lat'],
                        station['lon']
                    ))
                
                logger.info(f"Inserted {len(stations)} real stations")
            else:
                logger.error("Real station data file not found")
                return False
            
            # Load real trip data
            trip_file = os.path.join(self.data_dir, "202503-citibike-tripdata.csv.zip")
            if os.path.exists(trip_file):
                logger.info("Loading real trip data...")
                
                # Read the CSV file from zip
                with zipfile.ZipFile(trip_file, 'r') as zip_ref:
                    csv_filename = zip_ref.namelist()[0]
                    with zip_ref.open(csv_filename) as csv_file:
                        # Read in chunks to handle large file
                        chunk_size = 10000
                        trip_count = 0
                        
                        for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
                            # Process each chunk
                            for _, row in chunk.iterrows():
                                try:
                                    # Map CitiBike column names to our schema
                                    cursor.execute("""
                                        INSERT INTO trips (bike_id, start_station_id, end_station_id, started_at, ended_at)
                                        VALUES (?, ?, ?, ?, ?)
                                    """, (
                                        str(row.get('ride_id', 'unknown')),  # Use ride_id as bike_id
                                        str(row.get('start_station_id', '')),
                                        str(row.get('end_station_id', '')),
                                        row.get('started_at', ''),
                                        row.get('ended_at', '')
                                    ))
                                    trip_count += 1
                                    
                                    if trip_count % 10000 == 0:
                                        logger.info(f"Processed {trip_count} trips...")
                                        
                                except Exception as e:
                                    logger.warning(f"Skipping invalid trip row: {e}")
                                    continue
                
                logger.info(f"Inserted {trip_count} real trips")
            else:
                logger.warning("Real trip data file not found, using sample data")
                return False
            
            # Commit changes
            conn.commit()
            conn.close()
            
            logger.info("Successfully loaded real CitiBike data into database")
            return True
            
        except Exception as e:
            logger.error(f"Error loading real data to database: {e}")
            return False

def main():
    """
    Main function to run the data ingestion process
    """
    logger.info("Starting CitiBike data ingestion...")
    
    # Initialize ingestion
    ingestion = CitiBikeDataIngestion()
    
    # Check if real data files exist
    stations_file = os.path.join(ingestion.data_dir, "stations.json")
    trip_file = os.path.join(ingestion.data_dir, "202503-citibike-tripdata.csv.zip")
    
    if not os.path.exists(stations_file) or not os.path.exists(trip_file):
        logger.info("Real data files not found, downloading...")
        
        # Download data
        logger.info("Downloading trip data (3 months of historical data)...")
        trip_files = ingestion.download_trip_data(months=3)
        
        logger.info("Downloading station data...")
        station_file = ingestion.download_station_data()
        
        # Generate quality report
        logger.info("Generating data quality report...")
        report = ingestion.generate_quality_report(trip_files, station_file)
        
        # Save report
        report_path = os.path.join(ingestion.data_dir, "data_quality_report.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Data quality report saved to {report_path}")
    else:
        logger.info("Real data files already exist")
    
    # Load real data into database
    logger.info("Loading real data into database...")
    success = ingestion.load_real_data_to_database()
    
    if success:
        logger.info("✅ Successfully loaded real CitiBike data into database")
        logger.info("✅ Application now uses real CitiBike data instead of sample data")
    else:
        logger.error("❌ Failed to load real data into database")
        logger.warning("⚠️  Application will continue using sample data")

if __name__ == "__main__":
    main() 
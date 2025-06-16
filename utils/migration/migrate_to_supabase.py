#!/usr/bin/env python3
"""
Fast Local PostgreSQL to Supabase Migration Script using COPY

This script migrates data from local PostgreSQL database to Supabase
using PostgreSQL's native COPY command for maximum performance.

Usage:
    python migrate_to_supabase.py

Requirements:
    - Local PostgreSQL database with CitiBike data
    - Supabase project created and configured
    - Supabase DATABASE_URL environment variable set
"""

import os
import sys
import psycopg2
import time
import io
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add backend directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def get_database_connections():
    """Get connections to both local and Supabase databases."""
    try:
        # Local database connection (from environment or default)
        local_db_url = os.getenv('LOCAL_DATABASE_URL', 'postgresql://localhost/dev')
        local_conn = psycopg2.connect(local_db_url)
        
        # Supabase database connection
        supabase_db_url = os.getenv('SUPABASE_DATABASE_URL')
        if not supabase_db_url:
            print("❌ SUPABASE_DATABASE_URL environment variable not set")
            print("Please set SUPABASE_DATABASE_URL to your Supabase PostgreSQL connection string")
            return None, None
        
        supabase_conn = psycopg2.connect(supabase_db_url)
        
        return local_conn, supabase_conn
        
    except Exception as e:
        print(f"❌ Error connecting to databases: {e}")
        return None, None

def clear_supabase_tables(supabase_conn):
    """Clear existing data from Supabase tables."""
    try:
        cursor = supabase_conn.cursor()
        
        print("🧹 Clearing existing data from Supabase tables...")
        
        # Clear tables in reverse dependency order
        tables_to_clear = ['trips', 'station_mapping', 'stations']
        
        for table in tables_to_clear:
            cursor.execute(f"TRUNCATE TABLE {table} CASCADE")
            print(f"   ✅ Cleared {table} table")
        
        supabase_conn.commit()
        cursor.close()
        
        print("✅ All Supabase tables cleared successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error clearing Supabase tables: {e}")
        supabase_conn.rollback()
        return False

def create_supabase_schema(supabase_conn):
    """Create the database schema in Supabase."""
    try:
        cursor = supabase_conn.cursor()
        
        # Create stations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stations (
                id SERIAL PRIMARY KEY,
                station_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8)
            );
        """)
        
        # Create station_mapping table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS station_mapping (
                uuid_station_id VARCHAR(50) PRIMARY KEY,
                numeric_station_id VARCHAR(50) NOT NULL,
                station_name VARCHAR(255) NOT NULL
            );
        """)
        
        # Create trips table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                id SERIAL PRIMARY KEY,
                bike_id VARCHAR(50) NOT NULL,
                start_station_id VARCHAR(50) NOT NULL,
                end_station_id VARCHAR(50) NOT NULL,
                started_at TIMESTAMP NOT NULL,
                ended_at TIMESTAMP NOT NULL
            );
        """)
        
        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_trips_bike_id ON trips(bike_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_trips_stations ON trips(start_station_id, end_station_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_trips_time ON trips(started_at);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_station_mapping_numeric ON station_mapping(numeric_station_id);")
        
        supabase_conn.commit()
        cursor.close()
        
        print("✅ Supabase database schema created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating Supabase schema: {e}")
        supabase_conn.rollback()
        return False

def migrate_table_with_copy(local_conn, supabase_conn, table_name):
    """Migrate data from local table to Supabase table using COPY."""
    try:
        local_cursor = local_conn.cursor()
        supabase_cursor = supabase_conn.cursor()
        
        # Get total row count
        local_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_rows = local_cursor.fetchone()[0]
        
        print(f"📊 Migrating {table_name}: {total_rows:,} rows")
        
        # Get column names
        local_cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position")
        columns = [row[0] for row in local_cursor.fetchall()]
        
        # Skip 'id' column if it's auto-incrementing
        if 'id' in columns:
            columns.remove('id')
        
        columns_str = ', '.join(columns)
        
        # Export data from local database using COPY TO
        print(f"   📤 Exporting data from local {table_name}...")
        start_time = time.time()
        
        # Create a buffer to hold the CSV data
        csv_buffer = io.StringIO()
        
        # Use COPY TO to export data to CSV format
        local_cursor.copy_expert(
            f"COPY {table_name} ({columns_str}) TO STDOUT WITH CSV",
            csv_buffer
        )
        
        export_time = time.time() - start_time
        print(f"   ✅ Exported {total_rows:,} rows in {export_time:.1f} seconds")
        
        # Import data to Supabase using COPY FROM
        print(f"   📥 Importing data to Supabase {table_name}...")
        start_time = time.time()
        
        # Reset buffer position to beginning
        csv_buffer.seek(0)
        
        # Use COPY FROM to import data from CSV format
        supabase_cursor.copy_expert(
            f"COPY {table_name} ({columns_str}) FROM STDOUT WITH CSV",
            csv_buffer
        )
        
        # Commit the transaction
        supabase_conn.commit()
        
        import_time = time.time() - start_time
        print(f"   ✅ Imported {total_rows:,} rows in {import_time:.1f} seconds")
        
        # Close buffer and cursors
        csv_buffer.close()
        local_cursor.close()
        supabase_cursor.close()
        
        total_time = export_time + import_time
        print(f"✅ Successfully migrated {total_rows:,} rows from {table_name} in {total_time:.1f} seconds")
        return True
        
    except Exception as e:
        print(f"❌ Error migrating {table_name}: {e}")
        supabase_conn.rollback()
        return False

def verify_migration(local_conn, supabase_conn):
    """Verify that migration was successful by comparing row counts."""
    try:
        local_cursor = local_conn.cursor()
        supabase_cursor = supabase_conn.cursor()
        
        tables = ['stations', 'station_mapping', 'trips']
        
        print("\n🔍 Verifying migration...")
        
        for table in tables:
            # Get local row count
            local_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            local_count = local_cursor.fetchone()[0]
            
            # Get Supabase row count
            supabase_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            supabase_count = supabase_cursor.fetchone()[0]
            
            print(f"   {table}: {local_count:,} → {supabase_count:,} rows")
            
            if local_count != supabase_count:
                print(f"   ⚠️  WARNING: Row count mismatch for {table}")
                return False
        
        local_cursor.close()
        supabase_cursor.close()
        
        print("✅ Migration verification completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying migration: {e}")
        return False

def test_supabase_queries(supabase_conn):
    """Test some sample queries on Supabase to ensure data integrity."""
    try:
        cursor = supabase_conn.cursor()
        
        print("\n🧪 Testing Supabase queries...")
        
        # Test 1: Count total trips
        cursor.execute("SELECT COUNT(*) FROM trips")
        trip_count = cursor.fetchone()[0]
        print(f"   Total trips: {trip_count:,}")
        
        # Test 2: Count total stations
        cursor.execute("SELECT COUNT(*) FROM stations")
        station_count = cursor.fetchone()[0]
        print(f"   Total stations: {station_count:,}")
        
        # Test 3: Test station mapping
        cursor.execute("SELECT COUNT(*) FROM station_mapping")
        mapping_count = cursor.fetchone()[0]
        print(f"   Station mappings: {mapping_count:,}")
        
        # Test 4: Sample probability calculation query
        cursor.execute("""
            SELECT 
                s.name as station_name,
                COUNT(t.id) as trip_count
            FROM stations s
            JOIN station_mapping sm ON s.station_id = sm.uuid_station_id
            JOIN trips t ON sm.numeric_station_id = t.start_station_id
            GROUP BY s.name
            ORDER BY trip_count DESC
            LIMIT 5
        """)
        
        top_stations = cursor.fetchall()
        print("   Top 5 stations by trip count:")
        for station_name, trip_count in top_stations:
            print(f"     {station_name}: {trip_count:,} trips")
        
        cursor.close()
        
        print("✅ Supabase query tests completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Supabase queries: {e}")
        return False

def main():
    """Main migration function."""
    print("🚀 Starting FAST local PostgreSQL to Supabase migration using COPY...")
    print("=" * 80)
    
    # Get database connections
    print("\n🔗 Connecting to databases...")
    local_conn, supabase_conn = get_database_connections()
    
    if not local_conn or not supabase_conn:
        print("❌ Failed to connect to databases")
        return False
    
    print("✅ Connected to both local and Supabase databases")
    
    # Clear existing data from Supabase
    if not clear_supabase_tables(supabase_conn):
        print("❌ Failed to clear Supabase tables")
        return False
    
    # Create Supabase schema
    print("\n📋 Creating Supabase database schema...")
    if not create_supabase_schema(supabase_conn):
        print("❌ Failed to create Supabase schema")
        return False
    
    # Migrate data tables using COPY
    tables_to_migrate = ['stations', 'station_mapping', 'trips']
    
    print("\n📊 Starting fast data migration using COPY...")
    start_time = time.time()
    
    for table in tables_to_migrate:
        print(f"\n🔄 Migrating {table}...")
        if not migrate_table_with_copy(local_conn, supabase_conn, table):
            print(f"❌ Failed to migrate {table}")
            return False
    
    migration_time = time.time() - start_time
    print(f"\n⏱️  Migration completed in {migration_time:.1f} seconds")
    
    # Verify migration
    if not verify_migration(local_conn, supabase_conn):
        print("❌ Migration verification failed")
        return False
    
    # Test Supabase queries
    if not test_supabase_queries(supabase_conn):
        print("❌ Supabase query tests failed")
        return False
    
    # Close connections
    local_conn.close()
    supabase_conn.close()
    
    print("\n" + "=" * 80)
    print("✅ FAST local PostgreSQL to Supabase migration completed successfully!")
    print(f"⏱️  Total migration time: {migration_time:.1f} seconds")
    print("\n🚀 Ready for Vercel deployment!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
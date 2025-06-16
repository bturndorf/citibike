#!/usr/bin/env python3
"""
Script to check what tables are currently in the Railway PostgreSQL database
"""

import sys
from sqlalchemy import create_engine, text

# Railway PostgreSQL connection string from railway variables output
DATABASE_URL = "postgresql://postgres:gToMomZwJyYGcOzZGSRGGkLLkWSQXqzi@interchange.proxy.rlwy.net:44480/railway"

def check_railway_tables():
    """Connect to Railway PostgreSQL and check what tables exist"""
    
    print("🔍 Connecting to Railway PostgreSQL database...")
    
    try:
        # Create database engine
        engine = create_engine(DATABASE_URL)
        
        # Test connection and get table information
        with engine.connect() as conn:
            print("✅ Database connection successful")
            
            # Get PostgreSQL version
            version_result = conn.execute(text("SELECT version()"))
            version = version_result.scalar()
            print(f"📊 PostgreSQL Version: {version}")
            print()
            
            # Get list of all tables
            tables_result = conn.execute(text("""
                SELECT table_name, table_type 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables = tables_result.fetchall()
            
            if not tables:
                print("❌ No tables found in the database")
                return
            
            print(f"📋 Found {len(tables)} table(s) in Railway PostgreSQL database:")
            print("=" * 60)
            
            for table_name, table_type in tables:
                print(f"📄 {table_name} ({table_type})")
                
                # Get row count for each table
                try:
                    count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    count = count_result.scalar()
                    print(f"   └─ Rows: {count:,}")
                except Exception as e:
                    print(f"   └─ Error getting count: {e}")
                
                # Get table size
                try:
                    size_result = conn.execute(text(f"""
                        SELECT pg_size_pretty(pg_total_relation_size('{table_name}'))
                    """))
                    size = size_result.scalar()
                    print(f"   └─ Size: {size}")
                except Exception as e:
                    print(f"   └─ Error getting size: {e}")
                
                print()
            
            # Get database size
            try:
                db_size_result = conn.execute(text("""
                    SELECT pg_size_pretty(pg_database_size(current_database()))
                """))
                db_size = db_size_result.scalar()
                print(f"💾 Total database size: {db_size}")
            except Exception as e:
                print(f"💾 Error getting database size: {e}")
            
            print("=" * 60)
            
            # Check for specific tables we expect
            expected_tables = ['stations', 'trips', 'station_mapping']
            found_tables = [table[0] for table in tables]
            
            print("🔍 Checking for expected tables:")
            for expected_table in expected_tables:
                if expected_table in found_tables:
                    print(f"✅ {expected_table} - Found")
                else:
                    print(f"❌ {expected_table} - Missing")
            
            print()
            
            # If we have trips table, get some sample data info
            if 'trips' in found_tables:
                print("📊 Trips table sample information:")
                try:
                    # Get date range
                    date_result = conn.execute(text("""
                        SELECT MIN(started_at), MAX(started_at) 
                        FROM trips 
                        WHERE started_at IS NOT NULL
                    """))
                    min_date, max_date = date_result.fetchone()
                    print(f"   └─ Date range: {min_date} to {max_date}")
                    
                    # Get unique bikes count
                    bikes_result = conn.execute(text("SELECT COUNT(DISTINCT bike_id) FROM trips"))
                    bikes_count = bikes_result.scalar()
                    print(f"   └─ Unique bikes: {bikes_count:,}")
                    
                except Exception as e:
                    print(f"   └─ Error getting trips info: {e}")
            
            # If we have stations table, get some sample data info
            if 'stations' in found_tables:
                print("🏪 Stations table sample information:")
                try:
                    # Get sample station names
                    stations_result = conn.execute(text("""
                        SELECT name FROM stations LIMIT 5
                    """))
                    station_names = [row[0] for row in stations_result.fetchall()]
                    print(f"   └─ Sample stations: {', '.join(station_names)}")
                    
                except Exception as e:
                    print(f"   └─ Error getting stations info: {e}")
            
            # If we have station_mapping table, get some sample data info
            if 'station_mapping' in found_tables:
                print("🗺️ Station mapping table sample information:")
                try:
                    # Get mapping count
                    mapping_result = conn.execute(text("SELECT COUNT(*) FROM station_mapping"))
                    mapping_count = mapping_result.scalar()
                    print(f"   └─ Total mappings: {mapping_count:,}")
                    
                    # Get sample mappings
                    sample_result = conn.execute(text("""
                        SELECT station_name, uuid_station_id, numeric_station_id 
                        FROM station_mapping LIMIT 3
                    """))
                    samples = sample_result.fetchall()
                    for name, uuid_id, numeric_id in samples:
                        print(f"   └─ {name}: UUID={uuid_id[:8]}..., Numeric={numeric_id}")
                    
                except Exception as e:
                    print(f"   └─ Error getting mapping info: {e}")
            
    except Exception as e:
        print(f"❌ Error connecting to Railway database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚂 Railway PostgreSQL Database Table Check")
    print("=" * 60)
    success = check_railway_tables()
    
    if success:
        print("\n✅ Database check completed successfully")
    else:
        print("\n❌ Database check failed")
        sys.exit(1) 
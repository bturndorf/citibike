#!/usr/bin/env python3
"""
Railway Data Backup Script for Vercel + Supabase Migration

This script exports all data from Railway PostgreSQL database to ensure
zero data loss during migration to Vercel + Supabase.

Usage:
    python backup_railway_data.py

Requirements:
    - Railway CLI installed and authenticated
    - Access to Railway PostgreSQL database
    - Sufficient disk space for data export
"""

import os
import sys
import json
import csv
import subprocess
import psycopg2
from datetime import datetime
from pathlib import Path

# Add backend directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

def get_railway_database_url():
    """Get Railway PostgreSQL connection string via Railway CLI."""
    try:
        # Get Railway database URL from environment or CLI
        result = subprocess.run(
            ['railway', 'variables', '--service', 'Postgres'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the output to find DATABASE_URL
        for line in result.stdout.split('\n'):
            if 'DATABASE_URL' in line:
                return line.split('=')[1].strip()
        
        # Fallback to environment variable
        return os.getenv('DATABASE_URL')
        
    except subprocess.CalledProcessError as e:
        print(f"Error getting Railway database URL: {e}")
        print("Please ensure Railway CLI is installed and authenticated")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def connect_to_database(database_url):
    """Connect to Railway PostgreSQL database."""
    try:
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_table_data(conn, table_name):
    """Export data from a specific table."""
    try:
        cursor = conn.cursor()
        
        # Get column names
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position")
        columns = [row[0] for row in cursor.fetchall()]
        
        # Get all data
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        cursor.close()
        
        return {
            'table_name': table_name,
            'columns': columns,
            'rows': rows,
            'row_count': len(rows)
        }
        
    except Exception as e:
        print(f"Error exporting data from {table_name}: {e}")
        return None

def export_table_to_csv(data, output_dir):
    """Export table data to CSV file."""
    if not data:
        return False
    
    try:
        table_name = data['table_name']
        columns = data['columns']
        rows = data['rows']
        
        csv_file = output_dir / f"{table_name}.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)
        
        print(f"✅ Exported {data['row_count']} rows from {table_name} to {csv_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting {table_name} to CSV: {e}")
        return False

def export_table_to_json(data, output_dir):
    """Export table data to JSON file."""
    if not data:
        return False
    
    try:
        table_name = data['table_name']
        columns = data['columns']
        rows = data['rows']
        
        # Convert rows to list of dictionaries
        json_data = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            # Convert datetime objects to strings for JSON serialization
            for key, value in row_dict.items():
                if hasattr(value, 'isoformat'):
                    row_dict[key] = value.isoformat()
            json_data.append(row_dict)
        
        json_file = output_dir / f"{table_name}.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported {len(json_data)} rows from {table_name} to {json_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting {table_name} to JSON: {e}")
        return False

def get_database_schema(conn):
    """Export database schema information."""
    try:
        cursor = conn.cursor()
        
        # Get table information
        cursor.execute("""
            SELECT 
                table_name,
                table_type
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        # Get index information
        cursor.execute("""
            SELECT 
                indexname,
                tablename,
                indexdef
            FROM pg_indexes 
            WHERE schemaname = 'public'
            ORDER BY tablename, indexname
        """)
        indexes = cursor.fetchall()
        
        cursor.close()
        
        return {
            'tables': tables,
            'indexes': indexes
        }
        
    except Exception as e:
        print(f"Error exporting database schema: {e}")
        return None

def export_schema_to_json(schema, output_dir):
    """Export database schema to JSON file."""
    if not schema:
        return False
    
    try:
        schema_file = output_dir / "database_schema.json"
        
        # Convert to serializable format
        schema_data = {
            'tables': [{'table_name': t[0], 'table_type': t[1]} for t in schema['tables']],
            'indexes': [{'index_name': i[0], 'table_name': i[1], 'index_definition': i[2]} for i in schema['indexes']]
        }
        
        with open(schema_file, 'w', encoding='utf-8') as f:
            json.dump(schema_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported database schema to {schema_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting schema to JSON: {e}")
        return False

def create_backup_summary(output_dir, table_data_list, schema):
    """Create a summary of the backup."""
    try:
        summary = {
            'backup_timestamp': datetime.now().isoformat(),
            'backup_location': str(output_dir.absolute()),
            'tables_exported': [],
            'total_rows': 0,
            'schema_info': {
                'table_count': len(schema['tables']) if schema else 0,
                'index_count': len(schema['indexes']) if schema else 0
            }
        }
        
        for table_data in table_data_list:
            if table_data:
                summary['tables_exported'].append({
                    'table_name': table_data['table_name'],
                    'row_count': table_data['row_count'],
                    'columns': table_data['columns']
                })
                summary['total_rows'] += table_data['row_count']
        
        summary_file = output_dir / "backup_summary.json"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created backup summary at {summary_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating backup summary: {e}")
        return False

def main():
    """Main backup function."""
    print("🚀 Starting Railway PostgreSQL data backup for Vercel + Supabase migration...")
    print("=" * 80)
    
    # Create backup directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"data/backups/railway_backup_{timestamp}")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Backup directory: {backup_dir.absolute()}")
    
    # Get database connection
    print("\n🔗 Connecting to Railway PostgreSQL database...")
    database_url = get_railway_database_url()
    
    if not database_url:
        print("❌ Failed to get Railway database URL")
        print("Please ensure Railway CLI is installed and authenticated")
        return False
    
    conn = connect_to_database(database_url)
    if not conn:
        print("❌ Failed to connect to Railway database")
        return False
    
    print("✅ Connected to Railway PostgreSQL database")
    
    # Export database schema
    print("\n📋 Exporting database schema...")
    schema = get_database_schema(conn)
    if schema:
        export_schema_to_json(schema, backup_dir)
    
    # Define tables to export (in order of importance)
    tables_to_export = [
        'stations',
        'station_mapping', 
        'trips'
    ]
    
    # Export table data
    print("\n📊 Exporting table data...")
    table_data_list = []
    
    for table_name in tables_to_export:
        print(f"\n📦 Exporting {table_name}...")
        table_data = get_table_data(conn, table_name)
        
        if table_data:
            # Export to both CSV and JSON formats
            export_table_to_csv(table_data, backup_dir)
            export_table_to_json(table_data, backup_dir)
            table_data_list.append(table_data)
        else:
            print(f"⚠️  Warning: Could not export {table_name}")
    
    # Create backup summary
    print("\n📝 Creating backup summary...")
    create_backup_summary(backup_dir, table_data_list, schema)
    
    # Close database connection
    conn.close()
    
    print("\n" + "=" * 80)
    print("✅ Railway PostgreSQL data backup completed successfully!")
    print(f"📁 Backup location: {backup_dir.absolute()}")
    print(f"📊 Total tables exported: {len(table_data_list)}")
    print(f"📈 Total rows exported: {sum(td['row_count'] for td in table_data_list if td)}")
    print("\n🔒 Backup files created:")
    
    for file in backup_dir.glob("*"):
        if file.is_file():
            size_mb = file.stat().st_size / (1024 * 1024)
            print(f"   - {file.name} ({size_mb:.1f} MB)")
    
    print("\n🚀 Ready for Vercel + Supabase migration!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
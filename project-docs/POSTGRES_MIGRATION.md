# PostgreSQL Migration Guide

This guide helps you migrate the CitiBike application from SQLite to PostgreSQL for local development, aligning with the production Railway environment.

## Why Migrate to PostgreSQL?

Based on the insights from **Task 9** in the project plan, we identified a critical issue:

- **Local development**: SQLite (doesn't support PostgreSQL syntax like `EXTRACT(EPOCH FROM ...)`)
- **Railway production**: PostgreSQL (supports the syntax we're using)
- **Problem**: Code that works in production fails locally due to database technology mismatch

## Prerequisites

1. **PostgreSQL Installation**
   ```bash
   # macOS
   brew install postgresql
   brew services start postgresql
   
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   sudo systemctl start postgresql
   
   # Windows
   # Download from https://www.postgresql.org/download/windows/
   ```

2. **Python Dependencies**
   ```bash
   pip install psycopg2-binary python-dotenv
   ```

## Migration Steps

### Step 1: Set Up Local Environment

Run the environment setup script:
```bash
cd backend
python setup_local_env.py
```

This will:
- Create a `.env` file with PostgreSQL configuration
- Print detailed setup instructions

### Step 2: Create PostgreSQL Database

Run the PostgreSQL setup script:
```bash
python setup_local_postgres.py
```

This will:
- Check PostgreSQL installation
- Create `citibike_dev` database
- Create necessary tables and indexes
- Set up the `station_mapping` table

### Step 3: Migrate Data (Optional)

If you have existing SQLite data you want to preserve:
```bash
python migrate_data_to_postgres.py
```

This will:
- Migrate stations from SQLite to PostgreSQL
- Migrate trips in batches for performance
- Create station mappings
- Verify the migration

### Step 4: Test the Application

Start the application:
```bash
python main.py
```

The application should now:
- Connect to PostgreSQL instead of SQLite
- Use the same database technology as production
- Support PostgreSQL-specific SQL syntax

## Database Schema

The PostgreSQL schema includes:

### Tables
- **stations**: CitiBike station information
- **trips**: Trip data with bike movements
- **station_mapping**: Maps UUID station IDs to numeric IDs

### Indexes
- `idx_trips_bike_id`: For bike-based queries
- `idx_trips_stations`: For station-based queries
- `idx_trips_time`: For time-based queries
- `idx_station_mapping_numeric`: For station mapping lookups

## Environment Configuration

The `.env` file contains:
```env
DATABASE_URL=postgresql://postgres@localhost:5432/citibike_dev
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:3000"]
LOG_LEVEL=INFO
```

## Key Changes Made

### 1. Database Connection
- Updated `main.py` to use environment variables
- Removed SQLite-specific connection arguments
- Added PostgreSQL connection handling

### 2. Alembic Configuration
- Updated `alembic.ini` to use environment variables
- Modified `alembic/env.py` to load from `.env`
- Added fallback to SQLite for backward compatibility

### 3. SQL Compatibility
- All SQL queries now work with both SQLite and PostgreSQL
- PostgreSQL-specific syntax (like `EXTRACT(EPOCH FROM ...)`) now works locally
- Station mapping table resolves UUID/numeric ID mismatches

## Troubleshooting

### PostgreSQL Connection Issues
```bash
# Check if PostgreSQL is running
ps aux | grep postgres

# Check if database exists
psql -U postgres -l

# Create database manually if needed
createdb -U postgres citibike_dev
```

### Permission Issues
```bash
# macOS: Create postgres user if needed
createuser -s postgres

# Ubuntu: Switch to postgres user
sudo -u postgres psql
```

### Data Migration Issues
- Ensure SQLite database exists: `./dev.db`
- Check available disk space for PostgreSQL
- Monitor migration progress in logs

## Verification

After migration, verify:

1. **Database Connection**
   ```bash
   python -c "from main import engine; print('Connected successfully')"
   ```

2. **Data Integrity**
   ```bash
   python utils/database_stats.py
   ```

3. **API Functionality**
   ```bash
   curl http://localhost:8000/api/health
   curl http://localhost:8000/api/stations
   ```

## Benefits

1. **Consistency**: Local and production environments use the same database technology
2. **Compatibility**: PostgreSQL-specific SQL syntax works everywhere
3. **Performance**: PostgreSQL handles large datasets better than SQLite
4. **Features**: Access to PostgreSQL-specific features and optimizations
5. **Debugging**: Issues can be reproduced locally that occur in production

## Rollback

If you need to rollback to SQLite:
1. Set `DATABASE_URL=sqlite:///./dev.db` in `.env`
2. Restart the application
3. The application will fall back to SQLite

## Next Steps

After successful migration:
1. Update any remaining SQLite-specific code
2. Test all API endpoints
3. Verify probability calculations work correctly
4. Update documentation and deployment guides

---

**Note**: This migration aligns with the Railway production environment, ensuring that local development matches production behavior exactly. 
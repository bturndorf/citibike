# Utilities

This folder contains utility scripts for the CitiBike project.

## Database Utilities

### `database_stats.py`

A comprehensive database statistics utility for monitoring Railway PostgreSQL database state.

**Usage:**
```bash
# Basic database statistics
python utils/database_stats.py

# Include table structure information
python utils/database_stats.py --structure
```

**Features:**
- ✅ Trip and station counts
- ✅ Date range information
- ✅ Table size information
- ✅ Expected data threshold validation
- ✅ Table structure inspection (with --structure flag)
- ✅ Automatic DATABASE_URL detection from environment or .env

**Requirements:**
- `sqlalchemy`
- `python-dotenv`

**Setup:**
1. Install dependencies: `pip install sqlalchemy python-dotenv`
2. Set `DATABASE_URL` in your `.env` file, or export it as an environment variable.
3. Run the script from the project root.

**Troubleshooting:**
- If you see `DATABASE_URL not found in environment variables or .env file`, run `railway variables` to get the connection string and add it to your `.env` file:
  ```
  DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<db>
  ```
- The script will not use any hardcoded connection string for security and best practices.

**Example Output:**
```
📊 Trips count: 1,330,000
🏪 Stations count: 2,234
📅 Date range: 2025-02-28 08:43:52 to 2025-03-14 19:59:59
💾 Table sizes - Trips: 156 MB, Stations: 256 kB
✅ Trip count meets expected threshold (1.3M+)
✅ Station count meets expected threshold (2K+)
```

## Future Utilities

This folder can be expanded with additional utilities such as:
- Data validation scripts
- Performance monitoring tools
- Backup and restore utilities
- Migration helpers 
# Project Plan: CitiBike Rider Probability Application (MVP)

## 1. Project Overview

### 1.1 MVP Infrastructure: Vercel + Supabase (Recommended)
- **Platform**: Vercel.app (frontend) + Supabase.com (backend & database)
- **Database**: Supabase PostgreSQL (managed, real-time)
- **Backend**: Python FastAPI on Vercel Serverless Functions
- **Frontend**: Next.js deployed to Vercel
- **Deployment**: Simple git push (no complex CI/CD needed)

**Migration Rationale:**
- **Railway Issues**: Deploy failures, PostgreSQL service problems, storage constraints
- **Vercel Benefits**: Excellent Next.js support, fast deployments, reliable infrastructure
- **Supabase Benefits**: Better PostgreSQL management, real-time features, superior reliability
- **Development Velocity**: Eliminate Railway debugging time, focus on application features

## 2. Detailed Task Breakdown (MVP)

### Phase 1: Infrastructure Setup

#### Vercel + Supabase Setup
**Tasks:**
1. **Vercel Account Setup**
   - Create Vercel account (vercel.com)
   - Connect GitHub repository
   - Set up new project

2. **Supabase Database Setup**
   - Create Supabase account (supabase.com)
   - Create new project
   - Get connection string from dashboard
   - Test database connection

3. **Basic Backend Deployment**
   - Create simple FastAPI "Hello World" app
   - Deploy to Vercel Serverless Functions
   - Verify deployment works

**Deliverables:**
- Vercel project with Supabase database
- Working backend endpoint
- Basic deployment workflow

#### Project Structure & Local Development
**Tasks:**
1. **Project Structure Setup**
   - Create backend and frontend directories
   - Set up local development environment
   - Create basic requirements.txt and package.json

2. **Database Schema Design**
   - Design simple MVP schema
   - Create migration scripts
   - Test locally

3. **Environment Configuration**
   - Set up environment variables
   - Configure local vs production settings
   - Set up Vercel and Supabase environment variables

**Deliverables:**
- Complete project structure
- Database schema
- Local development environment

### Phase 2: Data Ingestion & Processing

#### Data Source Analysis
**Tasks:**
1. **CitiBike Data Download**
   - Download 3-6 months of CitiBike data
   - Analyze data structure and quality
   - Identify required transformations

2. **Data Processing Script**
   - Create Python script for data cleaning
   - Handle missing data and outliers
   - Validate data integrity

**Deliverables:**
- Downloaded CitiBike dataset
- Data processing script
- Data quality report

#### Data Loading & Validation
**Tasks:**
1. **Database Population**
   - Load processed data into Supabase PostgreSQL
   - Create indexes for performance
   - Validate data integrity

2. **Data Analysis**
   - Calculate basic statistics
   - Analyze bike movement patterns
   - Create summary reports

3. **API Endpoints for Data**
   - Create endpoints for station list
   - Add trip statistics endpoint
   - Test with sample queries

**Deliverables:**
- Populated database with CitiBike data
- Basic API endpoints
- Data analysis summary

### Phase 3: Backend Development & Modeling

#### Probability Model Development
**Tasks:**
1. **Model Research & Design**
   - Research mathematical approaches
   - Design simple probability model
   - Define model parameters

2. **Basic Probability Calculator**
   - Implement simple probability calculation
   - Handle edge cases
   - Add input validation

**Deliverables:**
- Probability calculation engine
- Model documentation
- Basic validation

#### API Development & Testing
**Tasks:**
1. **Probability API Endpoint**
   - Create probability calculation endpoint
   - Add parameter validation
   - Implement error handling

2. **Model Testing**
   - Create test datasets
   - Validate model accuracy
   - Performance testing

3. **API Integration**
   - Connect all endpoints
   - Add basic caching
   - Deploy to Vercel

**Deliverables:**
- Working probability API
- Test results
- Deployed backend

### Phase 4: Frontend Development

#### Next.js Setup & Basic UI
**Tasks:**
1. **Next.js Application Setup**
   - Create Next.js application
   - Configure TypeScript
   - Set up Tailwind CSS

2. **Basic UI Components**
   - Create layout components
   - Implement form components
   - Add responsive design

**Deliverables:**
- Basic Next.js application
- Responsive UI framework
- Form components

#### Station Selection & Results Display (MVP)
**Tasks:**
1. **Alphabetized Combobox Dropdown for Station Selection**
   - Implement a dropdown (combobox) for users to select their home station
   - Ensure stations are alphabetized for easy searching
   - Remove map-based selection from MVP

2. **Results Display**
   - Design results section/page
   - Add probability visualization (optional for MVP)
   - Implement charts (optional for MVP)

**Deliverables:**
- Alphabetized combobox dropdown for station selection
- Results display
- Complete MVP frontend

### Phase 5: Integration, Testing & Deployment

#### Frontend-Backend Integration
**Tasks:**
1. **API Integration**
   - Connect frontend to backend API
   - Add error handling
   - Implement loading states

2. **End-to-End Testing**
   - Test complete user workflow
   - Validate probability calculations
   - Fix integration issues

**Deliverables:**
- Integrated application
- Test results
- Bug fixes

#### Vercel + Supabase Deployment & Documentation
**Tasks:**
1. **Production Deployment to Vercel + Supabase**
   - Deploy frontend to Vercel
   - Deploy backend to Vercel Serverless Functions
   - Configure production environment variables
   - Set up Vercel domains
   - Test production deployment
   - Verify database connections in production

2. **Documentation**
   - Create user documentation
   - Write technical documentation
   - Create Vercel + Supabase deployment guide
   - Document environment variable setup

3. **Final Testing & Launch**
   - Production testing on Vercel + Supabase
   - User acceptance testing
   - Launch preparation

**Deliverables:**
- Production-ready application on Vercel + Supabase
- Complete documentation
- Launch-ready system

### Phase 6: Critical Bug Fixes and UX Improvements

#### Route Restructuring and UX Enhancement
**Tasks:**
✅ 1. **Route Simplification**
   - Remove homepage (index.tsx) and make /calculate the only route
   - Redirect root path to /calculate
   - Update navigation and routing logic

✅ 2. **App Description Addition**
   - Add brief description to top of /calculate page
   - Text: "Figure out your chance of getting the same CitiBike twice, based on your ride frequency and home station."
   - Style appropriately with Tailwind CSS

✅ 3. **Stations API Fix**
   - Investigate 500 error for stations endpoint
   - Ensure stations.json data is properly accessible to frontend
   - Fix API endpoint to serve station data correctly
   - Verify combobox populates with actual station names

✅ 4. **Combobox Search Functionality**
   - Add search/filter functionality to station combobox
   - Implement real-time filtering as user types
   - Ensure performance with large number of stations
   - Add keyboard navigation support

✅ 5. **Probability API Error Resolution**
   - Debug and fix `JSON.parse: unexpected character at line 1 column 1 of the JSON data` error in frontend
   - Investigate and resolve 500 error on network requests to `/api/probability` endpoint
   - Check backend API response format and ensure proper JSON serialization
   - Verify API endpoint is correctly configured and responding
   - Test probability calculation endpoint with various input parameters
   - Add proper error handling and logging for debugging

✅ 6. **Data Source Verification**
   - Confirmed frontend and backend were previously using sample data
   - Loaded real CitiBike station and trip data into the database (2,234 stations, 3.1M trips)
   - Verified database now contains real data (not synthetic)
   - Application now uses real CitiBike data for all calculations

✅ 7. **Database Trip Count Investigation**
   - **ROOT CAUSE IDENTIFIED**: Station ID format mismatch between tables
   - **Stations table**: Uses UUID format (e.g., `ffae66ec-7c16-436f-bd0a-eedf81d580e7`)
   - **Trips table**: Uses numeric format (e.g., `6650.07`, `6432.11`)
   - **Result**: 0 matching stations between tables, breaking probability calculations
   - **Solution**: Created `station_mapping` table linking UUID to numeric IDs
   - **Mapping table**: 2,234 stations mapped, 2,143 start stations and 2,180 end stations now match
   - **Verification**: Join queries now work correctly (e.g., "W 21 St & 6 Ave" has 12,342 trips)

✅ 8. **Backend API Update for Station Mapping**
   - Update `/api/probability` endpoint to use station_mapping table for joins
   - Modify SQL queries to join stations → station_mapping → trips
   - Test probability calculations with known stations (e.g., "W 21 St & 6 Ave")
   - Verify API returns correct trip counts and bike counts
   - Add error handling for stations not found in mapping table

✅ 9. **Database Technology Alignment & Production Schema Update**
   - **CRITICAL ISSUE IDENTIFIED**: Database technology mismatch between local and production
   - **Local development**: SQLite (doesn't support PostgreSQL syntax like `EXTRACT(EPOCH FROM ...)`)
   - **Railway production**: PostgreSQL (supports the syntax we're using)
   - **Solution**: Migrate local development to PostgreSQL
   
   **Tasks:**
   ✅ 1. **Local PostgreSQL Migration** ✅ COMPLETED
      - Installed PostgreSQL 14 via Homebrew
      - Created local `dev` database
      - Migrated 3.1M trips from SQLite to PostgreSQL (~10 minutes with bulk inserts)
      - Updated Alembic config to use environment variables
      - Verified backend connects to PostgreSQL successfully
   
   ✅ 2. **Station Mapping Table Setup** ✅ COMPLETED
      - **ISSUE RESOLVED**: Station mapping table was empty (0 records)
      - **SOLUTION IMPLEMENTED**: Created `populate_station_mapping.py` script
      - **DATA POPULATED**: Successfully loaded 2,234 station mappings from stations.json
      - **MAPPING STRUCTURE**: UUID station_id → numeric_station_id → station_name
      - **VERIFICATION**: Mapping table now works correctly with trips table
      - **EXAMPLE**: "W 21 St & 6 Ave" (UUID: 66dc120f-0aca-11e7-82f6-3863bb44ef7c, Numeric: 6140.05) has 12,342 trips
   
   ✅ 3. **Probability Endpoint Format Alignment** ✅ COMPLETED
      - **ISSUE IDENTIFIED**: Frontend sends station names, backend expects UUIDs
      - **EXAMPLE**: Frontend sends "W 21 St & 6 Ave", backend expects "66dc120f-0aca-11e7-82f6-3863bb44ef7c"
      - **SOLUTION IMPLEMENTED**: Added `get_uuid_by_station_name()` function to prob_calc.py
      - **BACKEND UPDATE**: Modified `calculate_bike_movement_probability()` to accept station names or UUIDs
      - **LOGIC ADDED**: Auto-detects if input is UUID (36 chars with hyphens) or station name
      - **VERIFICATION COMPLETED**: 
         - ✅ Tested with station names: "W 21 St & 6 Ave", "Broadway & W 29 St", "E 17 St & Broadway"
         - ✅ Tested with UUID: "66dc120f-0aca-11e7-82f6-3863bb44ef7c"
         - ✅ Both formats return identical results (same station, same probability calculations)
         - ✅ Real CitiBike data being used (12,342 trips for W 21 St & 6 Ave, 6,992 trips for Broadway & W 29 St)
         - ✅ Station mapping table working correctly with 2,234 stations mapped
      - **RESULT**: Frontend can now send station names directly, backend auto-converts to UUIDs for database queries
   
   ✅ 4. **Production Database Schema Update**
      - **CRITICAL ISSUE IDENTIFIED**: Railway PostgreSQL database out of storage space ("No space left on device" error)
      - **CURRENT STATUS**: Database has 1.33M trips and 2,234 stations but missing station_mapping table
      - **SOLUTION**: Increase Railway shared memory size and complete migration
      
      **Tasks:**
      ✅ 1. **Railway CLI Service Variable Investigation**
         - ✅ **FINDINGS**: Railway CLI DOES support setting service variables via CLI
         - ✅ **COMMAND**: `railway variables --set "KEY=VALUE" --service SERVICE_NAME`
         - ✅ **EXAMPLE**: `railway variables --set "RAILWAY_SHM_SIZE_BYTES=800000000" --service Postgres`
         - ✅ **VERIFICATION**: Successfully set RAILWAY_SHM_SIZE_BYTES variable via CLI
         - ✅ **DOCUMENTATION**: Railway CLI supports both `--set` and `--service` options for variable management
         - ✅ **ALTERNATIVE**: Railway dashboard also available but CLI is more efficient for automation
      
      ✅ 2. **Storage Space Requirements Analysis**
         - ✅ **CURRENT RAILWAY DB**: 145 MB (152,281,571 bytes) with 1.33M trips, 2,234 stations
         - ✅ **LOCAL DEV DB**: 726 MB (760,759,075 bytes) with 3.1M trips, 2,234 stations
         - ✅ **ADDITIONAL STORAGE NEEDED**: 581 MB for complete migration (3.1M trips + station_mapping table)
         - ✅ **RECOMMENDED SHM SIZE**: 800 MB (800,000,000 bytes) with 10% buffer for safety
         - ✅ **CALCULATION**: 726 MB (full dataset) + 74 MB buffer = 800 MB total
         - ✅ **CONFIGURATION**: RAILWAY_SHM_SIZE_BYTES=800000000 successfully set via CLI
         - ✅ **VERIFICATION**: Storage increase applied, ready for migration
      
      ✅ 3. **Trips Table Completeness Verification**
         - Compare Railway trips count (1.33M) vs local development (3.1M)
         - Determine if Railway trips table is truncated or incomplete
         - If trips table needs updating, create subtask for full data migration
         - Document findings: Is trips table complete or needs migration?
         - Plan: Update migrate_production_schema.py to include trips data if needed
         - YES: the trips table is incomplete
      
      4. **Migration Script Updates**
         - Railway trips table is truncated, because the postgres service previously did not have enough storage
         - Update migrate_production_schema.py to include all trips data
         - Add trips table migration if needed (based on subtask 3 findings)
         - Update script to handle Railway storage constraints
         - Add error handling for storage-related failures
         - Include verification steps for both station_mapping and trips tables
      
      5. **Railway Storage Configuration**
         - Set RAILWAY_SHM_SIZE_BYTES variable in Railway dashboard or via CLI
         - Recommended: 500MB (524,288,000 bytes) or 1GB (1,048,576,000 bytes)
         - Restart Railway PostgreSQL service after variable change
         - Verify storage increase took effect
         - Document final configuration for future reference
      
      6. **Production Migration Execution**
         - Run updated migrate_production_schema.py script
         - Monitor migration progress and handle any errors
         - Verify station_mapping table creation and population
         - Verify trips table completeness (if migration needed)
         - Create database indexes for performance optimization
      
      7. **Migration Verification and Validation**
         - Count rows in Railway database: stations, trips, station_mapping
         - Compare with local development database counts
         - Verify station_mapping table functionality with join queries
         - Test probability calculations in production environment
         - Confirm all tables have expected data and relationships work correctly
      
      **Note**: Migration script `utils/data_processing/migrate_production_schema.py` created following cursor rules (database-batch-operations, railway-cli-usage, railway-database-inquiries). Script failed with "No space left on device" error - requires Railway shared memory size increase before proceeding.

10. **Frontend Station Data Update**
    - Verify frontend stations combobox still works with UUID station IDs
    - Test that station selection properly maps to numeric IDs for API calls
    - Ensure station names display correctly in dropdown
    - Test complete user workflow with fixed backend

11. **Test Infrastructure Setup & Automation**
    - **OBJECTIVE**: Establish comprehensive test infrastructure to prevent regressions
    - **GOAL**: Run tests automatically on code changes, database migrations, and deployments
    - **SCOPE**: Backend (Python/pytest), Frontend (Jest/React Testing Library), Integration (Playwright)
    
    **Tasks:**
    ✅ 1. **Backend Test Infrastructure Setup**
       - Add pytest and testing dependencies to backend/requirements.txt
       - Create pytest.ini configuration file
       - Set up test database configuration (separate from dev/prod)
       - Create test fixtures for database sessions and sample data
       - Implement test data seeding scripts
       - Add test environment variables (.env.test)
       - Create test runner script (run_backend_tests.py)
       - Add test coverage reporting with pytest-cov
    
    ✅ 2. **Frontend Test Infrastructure Setup**
       - Add Jest, React Testing Library, and testing dependencies to frontend/package.json
       - Create jest.config.js configuration
       - Set up test environment for Next.js
       - Create test utilities and mock data
       - Add test scripts to package.json (test, test:watch, test:coverage)
       - Configure test environment variables
       - Create test runner script (run_frontend_tests.py)
    
    3. **Integration Test Infrastructure Setup**
       - Add Playwright for end-to-end testing
       - Create playwright.config.js
       - Set up test database for integration tests
       - Create test scenarios for complete user workflows
       - Add integration test runner script
       - Configure test environment for Railway deployment testing
    
    4. **Test Data Management**
       - Create test database schema (simplified version of production)
       - Implement test data seeding scripts
       - Create sample station and trip data for testing
       - Add test data cleanup scripts
       - Ensure test data isolation from development/production
    
    5. **Test Automation Scripts**
       - Create root-level test runner (run_all_tests.py)
       - Add pre-commit test hooks
       - Create Railway deployment test scripts
       - Add test result reporting and notifications
       - Implement test failure handling and reporting
    
    ✅ 6. **Cursor AI Test Rule Creation**
       - Create .cursor/rules/test-automation.mdc rule
       - Define when tests should run (file changes, commits, deployments)
       - Specify test execution order and dependencies
       - Add test skipping conditions for local development
       - Define test failure handling and reporting requirements
    
    7. **Critical Test Scenarios Implementation**
       - **Backend API Tests**: All endpoints return correct responses
       - **Probability Calculation Tests**: Mathematical accuracy and edge cases
       - **Database Integration Tests**: Connection, queries, and data integrity
       - **Frontend Component Tests**: Rendering, user interactions, form validation
       - **Integration Tests**: Complete user workflows, API communication
       - **Performance Tests**: Response times, memory usage, database query performance
       
       **Immediate Test Infrastructure Fixes:**
       ✅ 7.1. **Fix Test Database Configuration**
          - Update conftest.py to use PostgreSQL instead of SQLite for test database
          - Configure TEST_DATABASE_URL environment variable for PostgreSQL test database
          - Ensure test database uses same PostgreSQL dialect as production
          - Fix datetime handling in test data (PostgreSQL accepts string formats)
       
       ✅ 7.2. **Fix Missing Probability Calculator Methods**
          - Add missing `is_uuid_format()` method to CitiBikeProbabilityCalculator class
          - Implement UUID format detection logic (36 chars with hyphens)
          - Add unit tests for UUID format validation
          - Ensure method works with both UUID and station name inputs
       
       ✅ 7.3. **Fix FastAPI TestClient Configuration**
          - Correct TestClient instantiation in conftest.py fixtures
          - Update test_client fixture to use proper FastAPI TestClient syntax
          - Fix app import and configuration for test environment
          - Ensure TestClient works with PostgreSQL database connections
          - Resolve httpx version compatibility issues (downgraded to 0.24.1)
          - Fix Python path issues in conftest.py by adding backend directory to sys.path

       ✅ 7.4. **Update Test Documentation and Automation Rules**
          - Update TESTING.md with specific CitiBike test infrastructure details
          - Update .cursor/rules/test-automation.mdc with actual test files and commands
          - Add specific troubleshooting guides for common test failures
          - Document AI agent-specific test execution guidelines
          - Include critical setup requirements and environment variables
          - Add test file organization and naming conventions

12. **Test Suite Implementation**
    - Define critical test scenarios (see section 8.1)
    - Set up testing framework (Jest/React Testing Library for frontend, pytest for backend)
    - Implement automated tests for core functionality
    - Add simple test automation (no complex CI/CD for MVP)

12. **Performance Optimization with Database Indexing**
    - **OBJECTIVE**: Reduce probability calculation time from 13+ seconds to 2-5 seconds
    - **GOAL**: Implement production-ready database indexing strategy with safe rollback capabilities
    - **SCOPE**: Database indexes, migration management, performance testing, rollback procedures
    
    **Status: ROLLED BACK** ✅ COMPLETED
    - **Reason**: Performance optimization approach was not achieving the desired results
    - **Action**: Successfully rolled back to previous state using manual index removal
    - **Result**: Database and application restored to pre-optimization state
    
    **Rollback Summary:**
    ✅ **Database Indexes Removed:**
       - `idx_trips_station_time` - Removed
       - `idx_trips_bike_end_time` - Removed  
       - `idx_trips_end_station_time` - Removed
       - `idx_station_mapping_station_name` - Removed
    
    ✅ **Files Removed:**
       - `utils/deployment_scripts/create_indexes.py` - Removed
       - `utils/deployment_scripts/remove_indexes.py` - Removed
       - `utils/testing_scripts/test_performance.py` - Removed
       - `utils/testing_scripts/test_database_performance.py` - Removed
       - `project-docs/PERFORMANCE_OPTIMIZATION_ROLLBACK_PLAN.md` - Removed
       - `backend/alembic/versions/add_performance_indexes.py` - Removed
    
    ✅ **Database State Restored:**
       - Alembic migration reverted to `c9217afd089b` (station_mapping table)
       - Original indexes restored: `idx_trips_bike_id`, `idx_trips_stations`, `idx_trips_time`, `idx_station_mapping_numeric`
       - Application functionality verified and working
    
    **Performance Analysis Results:**
    - **Database queries**: Individual queries were fast (0.1-1 second) with indexes
    - **API response time**: Still 16-22 seconds even with optimized database queries
    - **Root cause**: Performance bottleneck is in application logic, not database performance
    - **Conclusion**: Database indexing alone cannot solve the performance issue
    
    **Next Steps:**
    - Investigate application-level optimizations (caching, query optimization, algorithm improvements)
    - Consider alternative approaches to probability calculation
    - Focus on optimizing the application logic rather than database indexes

**Deliverables:**
- Comprehensive rollback plan and testing strategy ✅ COMPLETED
- Automated scripts for index management ✅ COMPLETED
- Performance improvement documentation ✅ COMPLETED
- Production-ready indexing implementation ✅ COMPLETED
- Performance monitoring and validation results (in progress)

### Phase 7: Railway to Vercel + Supabase Migration

#### Platform Migration Planning
**Tasks:**
1. **Migration Assessment and Planning**
   - **OBJECTIVE**: Migrate from Railway to Vercel + Supabase to resolve deployment issues
   - **GOAL**: Eliminate Railway debugging time and improve development velocity
   - **SCOPE**: Complete platform migration with zero data loss
   
   **Migration Rationale:**
   - **Railway Issues**: Deploy failures, PostgreSQL service problems, storage constraints
   - **Vercel Benefits**: Excellent Next.js support, fast deployments, reliable infrastructure
   - **Supabase Benefits**: Better PostgreSQL management, real-time features, superior reliability
   - **Development Velocity**: Eliminate Railway debugging time, focus on application features

2. **Pre-Migration Data Backup**
   - Export all data from Railway PostgreSQL (3.1M trips, 2,234 stations, station_mapping table)
   - Create database schema backup (tables, indexes, constraints)
   - Backup environment variables and configuration
   - Document current Railway setup for rollback reference
   - Verify data integrity before migration

3. **Vercel + Supabase Setup**
   - Create Vercel account and connect GitHub repository
   - Create Supabase project and configure PostgreSQL database
   - Set up Vercel project with Next.js and FastAPI serverless functions
   - Configure environment variables in both platforms
   - Test basic connectivity between Vercel and Supabase

**Deliverables:**
- Complete data backup from Railway
- Vercel + Supabase project setup
- Migration plan and rollback strategy

#### Database Migration
**Tasks:**
1. **Supabase Database Schema Setup**
   - Create database schema in Supabase (stations, trips, station_mapping tables)
   - Set up database indexes for performance optimization
   - Configure database constraints and relationships
   - Test schema with sample data
   - Verify PostgreSQL compatibility and features

2. **Data Migration Execution**
   - Import 3.1M trips from Railway backup to Supabase
   - Import 2,234 stations and station_mapping data
   - Verify data integrity after migration
   - Test database queries and performance
   - Create database indexes for optimal performance
   - Validate all table relationships work correctly

3. **Database Connection Updates**
   - Update backend code to use Supabase PostgreSQL connection
   - Update environment variables for Supabase DATABASE_URL
   - Test database connectivity from local development
   - Verify Alembic migrations work with Supabase
   - Update test database configuration for Supabase

**Deliverables:**
- Migrated database with all data intact
- Updated database connection configuration
- Verified database performance and functionality

#### Backend Migration
**Tasks:**
1. **FastAPI to Vercel Serverless Functions Migration**
   - Convert FastAPI app to Vercel serverless functions
   - Update API routes for Vercel serverless architecture
   - Configure Vercel.json for Python runtime
   - Update requirements.txt for Vercel compatibility
   - Test API endpoints in Vercel environment

2. **Environment Variable Migration**
   - Migrate Railway environment variables to Vercel
   - Update DATABASE_URL to point to Supabase
   - Configure CORS settings for Vercel deployment
   - Set up production environment variables
   - Test environment variable access in Vercel

3. **API Endpoint Testing**
   - Test all API endpoints in Vercel environment
   - Verify probability calculation endpoint works
   - Test stations endpoint with Supabase data
   - Validate error handling and response formats
   - Performance testing with real CitiBike data

**Deliverables:**
- Working FastAPI backend on Vercel
- All API endpoints functional with Supabase
- Updated environment configuration

#### Frontend Migration
**Tasks:**
1. **Next.js to Vercel Deployment**
   - Deploy Next.js frontend to Vercel
   - Update API endpoint URLs to point to Vercel backend
   - Configure Vercel build settings for Next.js
   - Set up environment variables for frontend
   - Test frontend deployment and functionality

2. **API Integration Updates**
   - Update frontend API calls to use Vercel backend URLs
   - Test station combobox with Supabase data
   - Verify probability calculation workflow
   - Test error handling and loading states
   - Validate complete user journey

3. **Frontend-Backend Integration Testing**
   - Test complete user workflow from station selection to results
   - Verify data flows correctly between frontend and backend
   - Test with real CitiBike data from Supabase
   - Validate responsive design and user experience
   - Performance testing for large station lists

**Deliverables:**
- Deployed Next.js frontend on Vercel
- Working frontend-backend integration
- Complete user workflow validation

#### Configuration and Documentation Updates
**Tasks:**
1. **Railway Configuration Removal**
   - Remove all railway.json configuration files
   - Delete Railway-specific deployment scripts
   - Remove Railway CLI dependencies
   - Clean up Railway environment variables
   - Archive Railway-specific documentation

2. **Vercel + Supabase Configuration**
   - Create vercel.json configuration files
   - Set up Supabase client configuration
   - Configure build and deployment settings
   - Set up environment variable management
   - Create deployment automation scripts

3. **Documentation Updates**
   - Update PROJECT_PLAN.md with Vercel + Supabase architecture
   - Replace old deployment guide with new deployment guides for Vercel + Supabase
   - Update README.md with new platform information
   - Update API documentation with new endpoints

4. **Cursor Rules Updates**
   - Update .cursor/rules/railway-cli-usage.mdc to Vercel/Supabase equivalents (if there is a Vercel or Supabase CLI)
   - Update .cursor/rules/postgresql-database.mdc for Supabase specifics
   - Create new rules for Vercel deployment and Supabase management
   - Update test automation rules for new platform
   - Remove Railway-specific rules and configurations

**Deliverables:**
- Clean codebase without Railway dependencies
- Complete Vercel + Supabase configuration
- Updated documentation and deployment guides
- Updated Cursor rules for new platform

#### Migration Verification and Rollback Planning
**Tasks:**
1. **Comprehensive Testing**
   - End-to-end testing of complete application
   - Performance testing with real CitiBike data
   - Database query performance validation
   - API response time testing
   - User workflow validation

2. **Rollback Strategy**
   - Keep Railway deployment running during migration
   - Document rollback procedures if issues arise
   - Maintain Railway data backup for emergency restoration
   - Test rollback procedures before final Railway shutdown
   - Plan for quick reversion if critical issues discovered

3. **Production Deployment**
   - Deploy to Vercel + Supabase production environment
   - Configure custom domains if needed
   - Set up monitoring and error tracking
   - Verify all functionality works in production
   - Monitor performance and stability

4. **Railway Shutdown**
   - Verify Vercel + Supabase deployment is stable
   - Export final data backup from Railway
   - Document Railway shutdown procedures
   - Remove Railway project and services
   - Update all external references to Railway URLs

**Deliverables:**
- Fully functional application on Vercel + Supabase
- Verified production deployment
- Complete Railway shutdown
- Migration success documentation

**Migration Success Criteria:**
- All functionality works identically to Railway deployment
- Performance is equal to or better than Railway
- Zero data loss during migration
- Development velocity improved (no more Railway debugging)
- Reliable deployment process with Vercel + Supabase

**Deliverables:**
- Complete platform migration from Railway to Vercel + Supabase
- Improved development velocity and reliability
- Updated documentation and configuration
- Production-ready application on new platform

## 3. Simplified Technical Architecture

### 3.1 MVP Stack
- **Frontend**: Next.js + TypeScript + Tailwind CSS
- **Backend**: Python + FastAPI + SQLAlchemy
- **Database**: PostgreSQL (Supabase)
- **Deployment**: Vercel (simple git push)
- **Maps**: Mapbox or Google Maps API (future enhancement)
- **Charts**: Chart.js or Recharts

### 3.2 Vercel + Supabase Deployment Architecture
```
GitHub Repository
       ↓
   Vercel.app
       ↓
┌─────────────────┐
│   Frontend      │  Next.js app
│   (Vercel)      │
└─────────────────┘
       ↓
┌─────────────────┐
│   Backend       │  FastAPI serverless functions
│   (Vercel)      │
└─────────────────┘
       ↓
┌─────────────────┐
│   PostgreSQL    │  Supabase database
│   (Supabase)    │
└─────────────────┘
```

### 3.3 Simplified Database Schema
```sql
-- Stations table
CREATE TABLE stations (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR(50) UNIQUE,
    name VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8)
);

-- Station mapping table (links UUID to numeric station IDs)
CREATE TABLE station_mapping (
    uuid_station_id VARCHAR(50) PRIMARY KEY,
    numeric_station_id VARCHAR(50) NOT NULL,
    station_name VARCHAR(255) NOT NULL
);

-- Trips table (simplified)
CREATE TABLE trips (
    id SERIAL PRIMARY KEY,
    bike_id VARCHAR(50),
    start_station_id VARCHAR(50),
    end_station_id VARCHAR(50),
    started_at TIMESTAMP,
    ended_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_trips_bike_id ON trips(bike_id);
CREATE INDEX idx_trips_stations ON trips(start_station_id, end_station_id);
CREATE INDEX idx_trips_time ON trips(started_at);
CREATE INDEX idx_station_mapping_numeric ON station_mapping(numeric_station_id);
```

### 3.4 API Endpoints (MVP)
```
GET /api/stations - List all stations
GET /api/probability - Calculate encounter probability
POST /api/calculate - Submit calculation parameters
GET /api/health - Health check
```

## 4. Vercel + Supabase Deployment Guide

### 4.1 Initial Setup
1. **Create Vercel Account**
   - Sign up at vercel.com
   - Connect GitHub repository
   - Create new project

2. **Create Supabase Account**
   - Sign up at supabase.com
   - Create new project
   - Get connection string from dashboard

3. **Configure Environment Variables**
   - Set DATABASE_URL for Supabase PostgreSQL connection
   - Set API keys and secrets
   - Configure production settings

### 4.2 Deployment Process
1. **Backend Deployment**
   ```bash
   # Deploy backend to Vercel
   git add .
   git commit -m "feat(backend): deploy to Vercel"
   git push origin main
   ```

2. **Frontend Deployment**
   - Vercel automatically detects Next.js
   - Configure build settings in Vercel dashboard
   - Set environment variables for API endpoints

3. **Database Setup**
   - Run migrations on Supabase PostgreSQL
   - Load initial data
   - Verify connections

### 4.3 Vercel + Supabase-Specific Considerations
- **Auto-deployment**: Vercel deploys on git push
- **Environment variables**: Set in Vercel dashboard
- **Domains**: Vercel provides custom domains
- **Scaling**: Vercel handles basic scaling automatically
- **Monitoring**: Basic monitoring included
- **Database**: Supabase provides managed PostgreSQL with real-time features

## 5. MVP Risk Mitigation

### 5.1 Technical Risks
- **Data Processing**: Start with smaller dataset (3 months)
- **Performance**: Use simple probability model initially
- **Deployment**: Vercel handles most complexity
- **Database**: Supabase PostgreSQL is managed and reliable

### 5.2 Business Risks
- **User Adoption**: Focus on core functionality
- **Data Quality**: Implement robust data validation

## 6. MVP Success Criteria

### 6.1 Technical Success
- Application runs without errors on Vercel + Supabase
- Probability calculations work correctly
- Users can input parameters and see results
- Simple deployment process works reliably
- Database connections are stable

### 6.2 User Success
- Users understand how to use the app
- Results are presented clearly
- App provides value to CitiBike users

### 6.3 Business Success
- App gains initial user traction
- Positive feedback from users
- Foundation for future enhancements

## 7. Post-MVP Enhancements

### 7.1 When to Add Complexity
- **More than 50 daily users**: Add caching
- **Database performance issues**: Optimize queries
- **Advanced features needed**: Add user accounts
- **Scale requirements**: Consider AWS migration
- **Map-based station selection**: Add interactive map for station selection

### 7.2 Future Features
- Advanced statistical modeling
- Real-time data integration
- Mobile app version
- Social features

## 8. Test Suite Planning

### 8.1 Critical Test Scenarios

#### Frontend Tests (React/Next.js)
1. **Component Rendering Tests**
   - Station combobox renders correctly
   - Form inputs accept valid data
   - Results display shows calculated probabilities
   - Loading states work properly

2. **User Interaction Tests**
   - Station search/filter functionality works
   - Form submission triggers API calls
   - Error messages display appropriately
   - Responsive design works on different screen sizes

3. **API Integration Tests**
   - Stations endpoint returns data correctly
   - Probability calculation endpoint works
   - Error handling for API failures
   - Data validation on form inputs

#### Backend Tests (Python/FastAPI)
1. **API Endpoint Tests**
   - GET /api/stations returns station list
   - POST /api/calculate processes requests correctly
   - GET /api/health returns healthy status
   - Error responses are properly formatted

2. **Probability Calculation Tests**
   - Calculations are mathematically correct
   - Edge cases are handled properly
   - Input validation works correctly
   - Performance is acceptable with large datasets

3. **Data Integrity Tests**
   - Database connections work properly
   - Data queries return expected results
   - Sample data vs real data is clearly distinguished
   - Data quality checks pass

#### Integration Tests
1. **End-to-End Workflow Tests**
   - Complete user journey from station selection to results
   - Data flows correctly between frontend and backend
   - Real CitiBike data is used in calculations
   - Application works in production environment on Vercel + Supabase

2. **Performance Tests**
   - Application loads within acceptable time limits
   - Large station lists don't cause performance issues
   - Probability calculations complete in reasonable time
   - Memory usage remains stable

### 8.2 Test Implementation Strategy
- **Frontend**: Jest + React Testing Library
- **Backend**: pytest + FastAPI TestClient
- **E2E**: Playwright or Cypress
- **Simple Automation**: Basic test scripts (no complex CI/CD for MVP)
- **Coverage**: Aim for 80%+ code coverage on critical paths

This simplified MVP approach focuses on getting a working application quickly with minimal infrastructure complexity. Vercel + Supabase provides a simple deployment platform that eliminates the need for complex AWS setup, CI/CD pipelines, or advanced monitoring systems. The deployment process is as simple as pushing to git, making it ideal for rapid development and iteration. 
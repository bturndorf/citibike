# Project Plan: CitiBike Rider Probability Application (MVP)

## 1. Project Overview

### 1.1 MVP Infrastructure: Railway (Recommended)
- **Platform**: Railway.app (simple deployment)
- **Database**: Railway PostgreSQL (included)
- **Backend**: Python FastAPI on Railway
- **Frontend**: Next.js deployed to Railway
- **Deployment**: Simple git push (no CI/CD needed)

## 2. Detailed Task Breakdown (MVP)

### Phase 1: Infrastructure Setup

#### Railway Setup
**Tasks:**
1. **Railway Account Setup**
   - Create Railway account (railway.app)
   - Connect GitHub repository
   - Set up new project

2. **Database Setup**
   - Add PostgreSQL service to Railway project
   - Get connection string from dashboard
   - Test database connection

3. **Basic Backend Deployment**
   - Create simple FastAPI "Hello World" app
   - Deploy to Railway
   - Verify deployment works

**Deliverables:**
- Railway project with PostgreSQL database
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
   - Load processed data into Railway PostgreSQL
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
   - Deploy to Railway

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

#### Deployment & Documentation
**Tasks:**
1. **Production Deployment**
   - Deploy frontend to Railway
   - Configure production environment
   - Test production deployment

2. **Documentation**
   - Create user documentation
   - Write technical documentation
   - Create deployment guide

3. **Final Testing & Launch**
   - Production testing
   - User acceptance testing
   - Launch preparation

**Deliverables:**
- Production-ready application
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

7. **Test Suite Implementation**
   - Define critical test scenarios (see section 7.1)
   - Set up testing framework (Jest/React Testing Library for frontend, pytest for backend)
   - Implement automated tests for core functionality
   - Add CI/CD pipeline for test automation

**Deliverables:**
- Simplified single-route application
- Clear app description
- Working stations combobox with search
- Verified real data usage
- Comprehensive test suite
- Automated testing pipeline

## 3. Simplified Technical Architecture

### 3.1 MVP Stack
- **Frontend**: Next.js + TypeScript + Tailwind CSS
- **Backend**: Python + FastAPI + SQLAlchemy
- **Database**: PostgreSQL (Railway)
- **Deployment**: Railway (simple git push)
- **Maps**: Mapbox or Google Maps API (future enhancement)
- **Charts**: Chart.js or Recharts

### 3.2 Simplified Database Schema
```sql
-- Stations table
CREATE TABLE stations (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR(50) UNIQUE,
    name VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8)
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
```

### 3.3 API Endpoints (MVP)
```
GET /api/stations - List all stations
GET /api/probability - Calculate encounter probability
POST /api/calculate - Submit calculation parameters
GET /api/health - Health check
```

## 4. MVP Risk Mitigation

### 4.1 Technical Risks
- **Data Processing**: Start with smaller dataset (3 months)
- **Performance**: Use simple probability model initially
- **Deployment**: Railway handles most complexity

### 4.2 Business Risks
- **User Adoption**: Focus on core functionality
- **Data Quality**: Implement robust data validation

## 5. MVP Success Criteria

### 5.1 Technical Success
- Application runs without errors
- Probability calculations work correctly
- Users can input parameters and see results
- Simple deployment process works reliably

### 5.2 User Success
- Users understand how to use the app
- Results are presented clearly
- App provides value to CitiBike users

### 5.3 Business Success
- App gains initial user traction
- Positive feedback from users
- Foundation for future enhancements

## 6. Post-MVP Enhancements

### 6.1 When to Add Complexity
- **More than 50 daily users**: Add caching
- **Database performance issues**: Optimize queries
- **Advanced features needed**: Add user accounts
- **Scale requirements**: Move to AWS
- **Map-based station selection**: Add interactive map for station selection

### 6.2 Future Features
- Advanced statistical modeling
- Real-time data integration
- Mobile app version
- Social features

## 7. Test Suite Planning

### 7.1 Critical Test Scenarios

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
   - Application works in production environment

2. **Performance Tests**
   - Application loads within acceptable time limits
   - Large station lists don't cause performance issues
   - Probability calculations complete in reasonable time
   - Memory usage remains stable

### 7.2 Test Implementation Strategy
- **Frontend**: Jest + React Testing Library
- **Backend**: pytest + FastAPI TestClient
- **E2E**: Playwright or Cypress
- **CI/CD**: GitHub Actions for automated testing
- **Coverage**: Aim for 80%+ code coverage on critical paths

This simplified MVP approach focuses on getting a working application quickly with minimal infrastructure complexity. Railway provides a simple deployment platform that eliminates the need for complex AWS setup, CI/CD pipelines, or advanced monitoring systems. 
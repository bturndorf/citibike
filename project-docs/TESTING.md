# CitiBike Testing Documentation

This document provides comprehensive guidelines for testing the CitiBike Probability Application.

## 🚨 CRITICAL SETUP - READ FIRST!

**If you're getting SQLite DateTime errors or ModuleNotFoundError, follow these exact steps:**

### 1. Set Environment Variable (REQUIRED)
```bash
# Set this BEFORE running any tests
export TEST_DATABASE_URL="postgresql://localhost:5432/citibike_test"
```

### 2. Create PostgreSQL Test Database (REQUIRED)
```bash
# Create the test database if it doesn't exist
createdb citibike_test
```

### 3. Verify Database Connection
```bash
# Test the connection
psql -d citibike_test -c "SELECT 1;"
```

### 4. Install Correct Dependencies
```bash
# Install specific versions to avoid compatibility issues
pip install httpx==0.24.1
pip install fastapi==0.104.1
pip install pytest==7.4.3
```

### 5. Run Tests from Correct Directory
```bash
# Always run from the backend directory
cd backend
python -m pytest tests/ -v
```

**Common Mistakes That Cause Errors:**
- ❌ Not setting `TEST_DATABASE_URL` environment variable
- ❌ Using SQLite instead of PostgreSQL for tests
- ❌ Running tests from wrong directory
- ❌ Using incompatible package versions
- ❌ Missing PostgreSQL test database

## 🚨 AI AGENT TEST FAILURE ANALYSIS

**Why tests work for developers but fail for AI agents:**

### 1. Environment Variable Issues
**Problem**: AI agents don't inherit environment variables from shell sessions
**Solution**: Always set environment variables explicitly in test scripts

### 2. Database Connection Fallback
**Problem**: When `TEST_DATABASE_URL` is not set, system falls back to SQLite
**Solution**: Ensure PostgreSQL test database is always used

### 3. SQL Syntax Compatibility
**Problem**: PostgreSQL-specific SQL syntax fails with SQLite
**Solution**: Use database-agnostic SQL or detect database type

### 4. Working Directory Issues
**Problem**: AI agents may run from different directories
**Solution**: Use absolute paths and proper directory navigation

## CitiBike Test Infrastructure Overview

Our test suite is specifically designed for the CitiBike Probability Application with the following components:

### Backend Test Files
```
backend/tests/
├── conftest.py                      # Pytest configuration and fixtures
├── test_probability_calculations.py # Core probability calculation tests
├── test_api_endpoints.py           # FastAPI endpoint tests
├── test_stations.py                # Station data and validation tests
├── test_probability.py             # Legacy probability tests
└── test_api.py                     # Integration API tests
```

### Frontend Test Files
```
frontend/__tests__/
├── components/
│   └── StationSelector.test.tsx    # Station selector component tests
├── pages/
│   └── calculate.test.tsx          # Main calculation page tests
└── integration/
    └── user-workflow.test.tsx      # End-to-end workflow tests
```

## Quick Start

### Run All Tests
```bash
python run_all_tests.py
```

### Run Specific Test Types
```bash
# Backend only
cd backend && python run_backend_tests.py

# Frontend only
cd frontend && npm test

# Specific backend test files
cd backend && python -m pytest tests/test_probability_calculations.py -v
cd backend && python -m pytest tests/test_api_endpoints.py -v
cd backend && python -m pytest tests/test_stations.py -v
```

## Backend Testing

### Setup
```bash
cd backend

# 🚀 Quick setup (recommended)
./setup_test_environment.sh

# Or manual setup:
pip install -r requirements.txt

# ⚠️ CRITICAL: Install specific versions for compatibility
pip install httpx==0.24.1
pip install fastapi==0.104.1
pip install pytest==7.4.3

# ⚠️ CRITICAL: Create PostgreSQL test database
createdb citibike_test

# ⚠️ CRITICAL: Set test database environment variable
export TEST_DATABASE_URL="postgresql://localhost:5432/citibike_test"
```

### Running Tests
```bash
# Run all backend tests
cd backend
python run_backend_tests.py

# Run with pytest directly
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### Test Categories

#### 1. Probability Calculation Tests (`test_probability_calculations.py`)
- Mathematical accuracy of probability calculations
- Edge cases and boundary conditions
- Different time patterns and frequencies
- Station name vs UUID handling
- Error handling for invalid inputs

#### 2. API Endpoint Tests (`test_api_endpoints.py`)
- Health check endpoint (`/health`)
- Stations endpoint (`/stations`)
- Probability calculation endpoint (`/calculate`)
- Error handling and validation
- Response format validation

#### 3. Station Data Tests (`test_stations.py`)
- Station data validation
- Database connection and session management
- Station mapping functionality
- UUID format validation
- Data integrity checks

#### 4. Integration Tests (`test_api.py`)
- End-to-end API workflows
- Complete user request/response cycles
- Error scenario handling
- Performance under load

### ⚠️ Common Issues and Solutions

#### 1. ModuleNotFoundError: No module named 'main'
**Problem**: Python can't find the main module in tests
**Solution**: Ensure `conftest.py` has sys.path setup at the very top:
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
# ... rest of imports
```

#### 2. TestClient instantiation errors
**Problem**: Incompatible httpx version causes TestClient failures
**Solution**: Use specific httpx version:
```bash
pip install httpx==0.24.1
```

#### 3. Database connection errors
**Problem**: Tests try to use SQLite instead of PostgreSQL
**Solution**: 
- Create PostgreSQL test database: `createdb citibike_test`
- Set environment variable: `export TEST_DATABASE_URL="postgresql://localhost:5432/citibike_test"`
- Ensure `pytest.ini` has correct database URL

#### 4. Missing model methods
**Problem**: Tests fail due to missing methods in models
**Solution**: Ensure all required methods exist in `models.py`:
- `StationMapping` model with `is_uuid_format()` method
- Proper database model relationships

#### 5. Datetime handling errors
**Problem**: SQLite vs PostgreSQL datetime differences
**Solution**: Use PostgreSQL for tests (already configured in `pytest.ini`)

#### 6. SQL Syntax Errors (EXTRACT function)
**Problem**: PostgreSQL-specific SQL syntax fails with SQLite
**Solution**: Code now detects database type and uses appropriate syntax

## Frontend Testing

### Setup
```bash
cd frontend
npm install
```

### Running Tests
```bash
# Run all frontend tests
cd frontend
npm test

# Run with coverage
npm run test:coverage

# Watch mode for development
npm run test:watch
```

### Test Categories

#### Component Tests
- `StationSelector.test.tsx`: Station selection component
- Rendering and display validation
- User interactions and state management
- Error handling and validation

#### Page Tests
- `calculate.test.tsx`: Main calculation page
- Complete user workflows
- API integration testing
- Form validation and submission

#### Integration Tests
- `user-workflow.test.tsx`: End-to-end user workflows
- Cross-component interactions
- API communication testing
- Complete user journeys

## Database Testing

### Test Database Setup
```bash
# Create test database
createdb citibike_test

# Set environment variable
export TEST_DATABASE_URL="postgresql://localhost:5432/citibike_test"

# Run database tests
cd backend && python -m pytest tests/test_stations.py -v
```

### Test Data Management
- Isolated PostgreSQL test database (`citibike_test`)
- Sample station data for testing
- Automatic cleanup after tests
- Data integrity validation

## Performance Testing

### Response Time Tests
- API endpoint response times
- Database query performance
- Probability calculation speed
- Frontend rendering performance

### Load Testing
- Multiple concurrent requests
- Large dataset handling
- Memory usage monitoring
- Database connection pooling

## Test Automation

### Pre-commit Hooks
Tests run automatically before commits:
```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Railway Deployment Tests
Tests run before deployment to Railway:
```bash
# Pre-deployment test suite
python run_all_tests.py --coverage

# Production verification
cd backend && python run_backend_tests.py
```

## Test Writing Guidelines

### Backend Test Guidelines

#### Test Structure
```python
import pytest
from fastapi.testclient import TestClient

@pytest.mark.api
class TestAPIEndpoints:
    def test_endpoint_name(self, test_client, populated_test_db):
        """Test description"""
        # Arrange
        request_data = {...}
        
        # Act
        response = test_client.post("/api/endpoint", json=request_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "expected_field" in data
```

#### Best Practices
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Test both success and failure cases
- Use fixtures for common setup
- Mock external dependencies

### Frontend Test Guidelines

#### Test Structure
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

describe('ComponentName', () => {
  it('should render correctly', () => {
    render(<Component />)
    expect(screen.getByText('Expected Text')).toBeInTheDocument()
  })

  it('should handle user interactions', async () => {
    const user = userEvent.setup()
    render(<Component />)
    
    await user.click(screen.getByRole('button'))
    expect(screen.getByText('Result')).toBeInTheDocument()
  })
})
```

#### Best Practices
- Test user interactions, not implementation details
- Use semantic queries (getByRole, getByLabelText)
- Mock API calls and external dependencies
- Test accessibility features
- Use data-testid sparingly

## Debugging Tests

### Common Issues

#### Backend Tests
```bash
# Database connection issues
export TEST_DATABASE_URL="postgresql://localhost:5432/citibike_test"

# Import errors
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"

# Test isolation issues
pytest tests/ --setup-show
```

#### Frontend Tests
```bash
# Dependency issues
npm install --force

# Test environment issues
npm run test -- --verbose

# Debug specific test
npm run test -- --testNamePattern="specific test name"
```

### Test Logs
- Backend: Check console output and logs/
- Frontend: Check Jest output and coverage/
- Integration: Check network requests and responses

## Coverage Requirements

### Minimum Coverage Targets
- **Backend API endpoints**: 90%+
- **Probability calculation logic**: 95%+
- **Database operations**: 85%+
- **Frontend components**: 80%+
- **Integration workflows**: 75%+

### Coverage Reports
```bash
# Backend coverage
cd backend
python -m pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html

# Frontend coverage
cd frontend
npm run test:coverage
open coverage/lcov-report/index.html
```

## Continuous Integration

### Railway Deployment
Tests run automatically before deployment:
1. Backend tests
2. Frontend tests
3. Integration tests
4. Performance tests

### Local Development
```bash
# Quick test before committing
python run_all_tests.py --skip-frontend

# Full test suite
python run_all_tests.py --coverage --verbose
```

## Test Data Management

### Sample Data
- **Stations**: 10-20 test stations with known characteristics
- **Trips**: 100-1000 sample trips with realistic patterns
- **Edge Cases**: Empty data, invalid data, boundary conditions

### Data Isolation
- Separate PostgreSQL test database (`citibike_test`)
- Automatic cleanup after tests
- No interference with development data
- Consistent test environment

## Troubleshooting

### Test Failures
1. Check test environment setup
2. Verify dependencies are installed
3. Check database connections
4. Review test data consistency
5. Check for race conditions

### Performance Issues
1. Monitor database query performance
2. Check for memory leaks
3. Verify test data size
4. Review test isolation

### Integration Issues
1. Verify services are running
2. Check network connectivity
3. Review API endpoint availability
4. Check environment variables

## 🚨 Common Error Analysis

### Error: `TypeError: SQLite DateTime type only accepts Python datetime and date objects as input`

**What happened:** The developer's tests were using SQLite instead of PostgreSQL, causing datetime handling errors.

**Root cause:** Missing `TEST_DATABASE_URL` environment variable, causing the test configuration to fall back to SQLite.

**Solution:**
```bash
# Set the environment variable BEFORE running tests
export TEST_DATABASE_URL="postgresql://localhost:5432/citibike_test"
```

### Error: `ModuleNotFoundError: No module named 'main'`

**What happened:** Python couldn't find the main module because the sys.path wasn't configured correctly.

**Root cause:** Missing `sys.path` setup in `conftest.py`.

**Solution:** Ensure `conftest.py` has this at the very top:
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
```

### Error: `TestClient instantiation errors`

**What happened:** Incompatible httpx version caused FastAPI TestClient to fail.

**Root cause:** Using newer httpx version that's incompatible with the current FastAPI version.

**Solution:**
```bash
pip install httpx==0.24.1
```

### Error: `Connection refused` in integration tests

**What happened:** Integration tests tried to connect to backend that wasn't running.

**Root cause:** Backend server wasn't started before running integration tests.

**Solution:**
```bash
# Terminal 1: Start backend
cd backend
python main.py

# Terminal 2: Run integration tests
cd backend && python -m pytest tests/test_api_endpoints.py -v
```

### Error: `(sqlite3.OperationalError) near "FROM": syntax error`

**What happened:** PostgreSQL-specific SQL syntax was used with SQLite database.

**Root cause:** Database type detection failed or environment variables not set.

**Solution:**
```bash
# Ensure PostgreSQL test database is used
export TEST_DATABASE_URL="postgresql://localhost:5432/citibike_test"
createdb citibike_test
```

## Quick Fix Checklist

If you're getting errors, run this checklist:

1. **Set environment variable:**
   ```bash
   export TEST_DATABASE_URL="postgresql://localhost:5432/citibike_test"
   ```

2. **Create test database:**
   ```bash
   createdb citibike_test
   ```

3. **Install correct dependencies:**
   ```bash
   pip install httpx==0.24.1
   pip install fastapi==0.104.1
   pip install pytest==7.4.3
   ```

4. **Run from correct directory:**
   ```bash
   cd backend
   python -m pytest tests/ -v
   ```

5. **Or use the setup script:**
   ```bash
   cd backend
   ./setup_test_environment.sh
   ```

## AI Agent Specific Guidelines

### For AI Agents Running Tests

1. **Always set environment variables explicitly:**
   ```python
   import os
   os.environ["TESTING"] = "true"
   os.environ["TEST_DATABASE_URL"] = "postgresql://localhost:5432/citibike_test"
   os.environ["DATABASE_URL"] = "postgresql://localhost:5432/citibike_dev"
   ```

2. **Use the setup script:**
   ```bash
   cd backend
   ./setup_test_environment.sh
   ```

3. **Run tests with proper environment:**
   ```bash
   cd backend
   ./run_tests.sh
   ```

4. **If tests fail, run troubleshooting:**
   ```bash
   cd backend
   ./troubleshoot_tests.sh
   ```

### Common AI Agent Mistakes

1. **Not setting environment variables** - Always set them explicitly
2. **Running from wrong directory** - Always `cd backend` first
3. **Using wrong database** - Always use PostgreSQL test database
4. **Missing dependencies** - Always run setup script first
5. **Not checking database connection** - Verify PostgreSQL is running

## Best Practices Summary

1. **Write tests first** (TDD approach)
2. **Test behavior, not implementation**
3. **Keep tests fast and isolated**
4. **Use descriptive test names**
5. **Maintain test data consistency**
6. **Run tests frequently**
7. **Monitor test coverage**
8. **Document test scenarios**
9. **Automate test execution**
10. **Review and refactor tests regularly**

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Next.js Testing](https://nextjs.org/docs/testing)

## Quick Troubleshooting Guide

### Immediate Issues and Solutions

#### 🔴 Tests won't start
```bash
# Check if test database exists
psql -l | grep citibike_test

# Create if missing
createdb citibike_test

# Set environment variable
export TEST_DATABASE_URL="postgresql://localhost:5432/citibike_test"
```

#### 🔴 Import errors in tests
```bash
# Check Python path in conftest.py
# Ensure this is at the very top:
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
```

#### 🔴 TestClient errors
```bash
# Fix httpx version
pip uninstall httpx
pip install httpx==0.24.1
```

#### 🔴 SQL syntax errors
```bash
# Ensure PostgreSQL is being used
export TEST_DATABASE_URL="postgresql://localhost:5432/citibike_test"
createdb citibike_test
```

#### 🔴 Database connection errors
```bash
# Check PostgreSQL is running
pg_isready

# Start PostgreSQL if needed
brew services start postgresql  # macOS
sudo systemctl start postgresql  # Linux
```
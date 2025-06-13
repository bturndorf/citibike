#!/bin/bash

# CitiBike Test Environment Setup Script
# This script ensures the test environment is properly configured

set -e  # Exit on any error

echo "🚀 Setting up CitiBike test environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the backend directory
if [ ! -f "main.py" ] || [ ! -d "tests" ]; then
    print_error "This script must be run from the backend directory"
    exit 1
fi

# 1. Check PostgreSQL availability
echo "Checking PostgreSQL availability..."
if command -v psql &> /dev/null; then
    print_status "PostgreSQL client found"
else
    print_warning "PostgreSQL client not found"
    print_warning "Tests may use SQLite fallback (not recommended)"
fi

# 2. Create test database
echo "Setting up test database..."
if command -v createdb &> /dev/null; then
    # Try to create the test database
    if createdb citibike_test 2>/dev/null; then
        print_status "Created PostgreSQL test database 'citibike_test'"
    else
        print_warning "Test database 'citibike_test' already exists or could not be created"
    fi
    
    # Test database connection
    if psql -d citibike_test -c "SELECT 1;" >/dev/null 2>&1; then
        print_status "Test database connection successful"
    else
        print_error "Cannot connect to test database. Please check PostgreSQL is running."
        print_error "On macOS: brew services start postgresql"
        print_error "On Linux: sudo systemctl start postgresql"
        exit 1
    fi
else
    print_warning "PostgreSQL client not available, tests may use SQLite fallback"
fi

# 3. Set environment variables
echo "Setting environment variables..."
export TESTING=true
export ENVIRONMENT=test
export TEST_DATABASE_URL="postgresql://localhost:5432/citibike_test"
export DATABASE_URL="postgresql://localhost:5432/citibike_dev"

# 4. Create .env file for tests if it doesn't exist
if [ ! -f ".env.test" ]; then
    cat > .env.test << EOF
TESTING=true
ENVIRONMENT=test
TEST_DATABASE_URL=postgresql://localhost:5432/citibike_test
DATABASE_URL=postgresql://localhost:5432/citibike_dev
EOF
    print_status "Created .env.test file"
fi

# 5. Create a test runner script
cat > run_tests.sh << 'EOF'
#!/bin/bash
# Test runner script with proper environment setup

# Set environment variables
export TESTING=true
export ENVIRONMENT=test
export TEST_DATABASE_URL="postgresql://localhost:5432/citibike_test"
export DATABASE_URL="postgresql://localhost:5432/citibike_dev"

# Run tests
echo "🧪 Running CitiBike backend tests..."
python -m pytest tests/ -v --tb=short

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed"
    exit 1
fi
EOF

chmod +x run_tests.sh
print_status "Created test runner script: run_tests.sh"

# 6. Create troubleshooting script
cat > troubleshoot_tests.sh << 'EOF'
#!/bin/bash
# Troubleshooting script for test issues

echo "🔍 CitiBike Test Troubleshooting"
echo "=================================="

echo "1. Environment Variables:"
echo "   TESTING: ${TESTING:-'NOT SET'}"
echo "   TEST_DATABASE_URL: ${TEST_DATABASE_URL:-'NOT SET'}"
echo "   DATABASE_URL: ${DATABASE_URL:-'NOT SET'}"

echo ""
echo "2. Database Connection:"
if command -v psql &> /dev/null; then
    if psql -d citibike_test -c "SELECT 1;" >/dev/null 2>&1; then
        echo "   ✅ PostgreSQL test database accessible"
    else
        echo "   ❌ Cannot connect to PostgreSQL test database"
    fi
else
    echo "   ⚠️  PostgreSQL client not found"
fi

echo ""
echo "3. Python Dependencies:"
python -c "
import sys
try:
    import fastapi
    print(f'   ✅ FastAPI {fastapi.__version__}')
except ImportError:
    print('   ❌ FastAPI not installed')

try:
    import httpx
    print(f'   ✅ httpx {httpx.__version__}')
except ImportError:
    print('   ❌ httpx not installed')

try:
    import pytest
    print(f'   ✅ pytest {pytest.__version__}')
except ImportError:
    print('   ❌ pytest not installed')
"

echo ""
echo "4. Test Database Tables:"
if command -v psql &> /dev/null; then
    psql -d citibike_test -c "\dt" 2>/dev/null || echo "   ❌ Cannot list tables"
fi

echo ""
echo "5. Quick Import Test:"
python -c "
import sys
sys.path.insert(0, '.')
try:
    from main import app
    from models import Base
    from prob_calc import CitiBikeProbabilityCalculator
    print('   ✅ All modules import successfully')
except Exception as e:
    print(f'   ❌ Import error: {e}')
"
EOF

chmod +x troubleshoot_tests.sh
print_status "Created troubleshooting script: troubleshoot_tests.sh"

echo ""
echo "🎉 Test environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Run tests: ./run_tests.sh"
echo "2. If tests fail: ./troubleshoot_tests.sh"
echo "3. For detailed test output: python -m pytest tests/ -v"
echo ""
echo "Environment variables set:"
echo "  TESTING=true"
echo "  TEST_DATABASE_URL=postgresql://localhost:5432/citibike_test"
echo "  DATABASE_URL=postgresql://localhost:5432/citibike_dev"
echo ""
echo "Note: These environment variables are set for this session only."
echo "To make them permanent, add them to your shell profile." 
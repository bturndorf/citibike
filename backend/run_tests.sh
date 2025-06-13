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

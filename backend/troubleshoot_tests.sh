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

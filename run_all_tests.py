#!/usr/bin/env python3
"""
CitiBike Test Suite Runner
Runs all tests with proper environment setup to ensure reliability
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path

def setup_environment():
    """Set up environment variables for reliable test execution"""
    print("🔧 Setting up test environment...")
    
    # Set critical environment variables
    os.environ["TESTING"] = "true"
    os.environ["ENVIRONMENT"] = "test"
    os.environ["TEST_DATABASE_URL"] = "postgresql://localhost:5432/citibike_test"
    os.environ["DATABASE_URL"] = "postgresql://localhost:5432/citibike_dev"
    
    # Ensure we're in the right directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print("✅ Environment variables set:")
    print(f"   TESTING: {os.environ.get('TESTING')}")
    print(f"   TEST_DATABASE_URL: {os.environ.get('TEST_DATABASE_URL')}")
    print(f"   DATABASE_URL: {os.environ.get('DATABASE_URL')}")

def check_database_connection():
    """Check if PostgreSQL test database is accessible"""
    print("🔍 Checking database connection...")
    
    try:
        # Try to connect to PostgreSQL test database
        result = subprocess.run([
            "psql", "-d", "citibike_test", "-c", "SELECT 1;"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ PostgreSQL test database accessible")
            return True
        else:
            print("❌ Cannot connect to PostgreSQL test database")
            print("   Error:", result.stderr)
            return False
            
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"⚠️  PostgreSQL client not available: {e}")
        print("   Tests will use SQLite fallback")
        return False

def create_test_database():
    """Create PostgreSQL test database if it doesn't exist"""
    print("📦 Creating test database...")
    
    try:
        # Try to create the test database
        result = subprocess.run([
            "createdb", "citibike_test"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Created PostgreSQL test database 'citibike_test'")
        else:
            print("⚠️  Test database 'citibike_test' already exists or could not be created")
            
    except FileNotFoundError:
        print("⚠️  PostgreSQL client not available, skipping database creation")

def run_backend_tests(verbose=False):
    """Run backend tests with proper setup"""
    print("=" * 50)
    print("RUNNING BACKEND TESTS")
    print("=" * 50)
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Set backend-specific environment
    os.environ["PYTHONPATH"] = str(backend_dir.absolute())
    
    # Run backend tests
    cmd = ["python", "-m", "pytest", "tests/", "-v"]
    if verbose:
        cmd.extend(["--tb=long", "--capture=no"])
    
    try:
        result = subprocess.run(cmd, env=os.environ, timeout=300)
        success = result.returncode == 0
        
        if success:
            print("✅ Backend tests passed")
        else:
            print("❌ Backend tests failed")
            
        return success
        
    except subprocess.TimeoutExpired:
        print("❌ Backend tests timed out")
        return False
    except Exception as e:
        print(f"❌ Backend tests failed with error: {e}")
        return False

def run_frontend_tests(verbose=False):
    """Run frontend tests"""
    print("=" * 50)
    print("RUNNING FRONTEND TESTS")
    print("=" * 50)
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Check if node_modules exists
    if not Path("node_modules").exists():
        print("📦 Installing frontend dependencies...")
        subprocess.run(["npm", "install"], check=True)
    
    # Run frontend tests
    try:
        cmd = ["npm", "test"]
        if verbose:
            cmd.extend(["--", "--verbose"])
            
        result = subprocess.run(cmd, env=os.environ, timeout=300)
        success = result.returncode == 0
        
        if success:
            print("✅ Frontend tests passed")
        else:
            print("❌ Frontend tests failed")
            
        return success
        
    except subprocess.TimeoutExpired:
        print("❌ Frontend tests timed out")
        return False
    except Exception as e:
        print(f"❌ Frontend tests failed with error: {e}")
        return False

def run_integration_tests(verbose=False):
    """Run integration tests"""
    print("=" * 50)
    print("RUNNING INTEGRATION TESTS")
    print("=" * 50)
    
    # Check if backend is running
    try:
        import requests
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
        else:
            print("❌ Backend server is not responding correctly")
            return False
    except Exception as e:
        print(f"❌ Backend server is not running: {e}")
        print("   Start the backend server first: cd backend && python main.py")
        return False
    
    # Run integration tests
    try:
        cmd = ["python", "-m", "pytest", "tests/integration/", "-v"]
        if verbose:
            cmd.extend(["--tb=long", "--capture=no"])
            
        result = subprocess.run(cmd, env=os.environ, timeout=300)
        success = result.returncode == 0
        
        if success:
            print("✅ Integration tests passed")
        else:
            print("❌ Integration tests failed")
            
        return success
        
    except subprocess.TimeoutExpired:
        print("❌ Integration tests timed out")
        return False
    except Exception as e:
        print(f"❌ Integration tests failed with error: {e}")
        return False

def run_database_tests(verbose=False):
    """Run database-specific tests"""
    print("=" * 50)
    print("RUNNING DATABASE TESTS")
    print("=" * 50)
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Run database tests
    try:
        cmd = ["python", "-m", "pytest", "tests/", "-m", "database", "-v"]
        if verbose:
            cmd.extend(["--tb=long", "--capture=no"])
            
        result = subprocess.run(cmd, env=os.environ, timeout=300)
        success = result.returncode == 0
        
        if success:
            print("✅ Database tests passed")
        else:
            print("❌ Database tests failed")
            
        return success
        
    except subprocess.TimeoutExpired:
        print("❌ Database tests timed out")
        return False
    except Exception as e:
        print(f"❌ Database tests failed with error: {e}")
        return False

def run_performance_tests(verbose=False):
    """Run performance tests"""
    print("=" * 50)
    print("RUNNING PERFORMANCE TESTS")
    print("=" * 50)
    
    # Check if backend is running
    try:
        import requests
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
        else:
            print("❌ Backend server is not responding correctly")
            return False
    except Exception as e:
        print(f"❌ Backend server is not running: {e}")
        print("   Start the backend server first: cd backend && python main.py")
        return False
    
    # Run performance tests
    try:
        cmd = ["python", "-m", "pytest", "tests/", "-m", "slow", "-v"]
        if verbose:
            cmd.extend(["--tb=long", "--capture=no"])
            
        result = subprocess.run(cmd, env=os.environ, timeout=600)  # 10 minutes for performance tests
        success = result.returncode == 0
        
        if success:
            print("✅ Performance tests passed")
        else:
            print("❌ Performance tests failed")
            
        return success
        
    except subprocess.TimeoutExpired:
        print("❌ Performance tests timed out")
        return False
    except Exception as e:
        print(f"❌ Performance tests failed with error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run CitiBike test suite")
    parser.add_argument("--backend-only", action="store_true", help="Run only backend tests")
    parser.add_argument("--frontend-only", action="store_true", help="Run only frontend tests")
    parser.add_argument("--integration-only", action="store_true", help="Run only integration tests")
    parser.add_argument("--database-only", action="store_true", help="Run only database tests")
    parser.add_argument("--performance-only", action="store_true", help="Run only performance tests")
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--skip-setup", action="store_true", help="Skip environment setup")
    
    args = parser.parse_args()
    
    # Setup environment
    if not args.skip_setup:
        setup_environment()
        create_test_database()
        check_database_connection()
    
    # Track results
    results = {}
    
    # Run tests based on arguments
    if args.backend_only:
        results["backend"] = run_backend_tests(args.verbose)
    elif args.frontend_only:
        results["frontend"] = run_frontend_tests(args.verbose)
    elif args.integration_only:
        results["integration"] = run_integration_tests(args.verbose)
    elif args.database_only:
        results["database"] = run_database_tests(args.verbose)
    elif args.performance_only:
        results["performance"] = run_performance_tests(args.verbose)
    else:
        # Run all tests
        results["backend"] = run_backend_tests(args.verbose)
        results["frontend"] = run_frontend_tests(args.verbose)
        results["integration"] = run_integration_tests(args.verbose)
        results["database"] = run_database_tests(args.verbose)
        results["performance"] = run_performance_tests(args.verbose)
    
    # Print summary
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for test_type, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_type.upper()}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("💥 SOME TESTS FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
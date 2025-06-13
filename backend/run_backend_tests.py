#!/usr/bin/env python3
"""
Backend test runner for CitiBike application
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

def setup_test_environment():
    """Set up test environment variables"""
    os.environ["TESTING"] = "true"
    os.environ["ENVIRONMENT"] = "test"
    
    # Use test database URL if provided, otherwise use SQLite
    if not os.getenv("TEST_DATABASE_URL"):
        os.environ["TEST_DATABASE_URL"] = "sqlite:///./test.db"

def run_pytest_tests(verbose=False, coverage=False, markers=None):
    """Run pytest tests with specified options"""
    cmd = ["python", "-m", "pytest", "tests/"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=.", "--cov-report=html", "--cov-report=term-missing"])
    
    if markers:
        cmd.extend(["-m", markers])
    
    print(f"Running pytest with command: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    return result.returncode

def run_legacy_tests():
    """Run legacy test scripts"""
    test_files = [
        "tests/test_api.py",
        "tests/test_probability.py",
        "tests/test_stations.py"
    ]
    
    results = []
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"\nRunning {test_file}...")
            result = subprocess.run(["python", test_file], cwd=Path(__file__).parent)
            results.append(result.returncode)
        else:
            print(f"Warning: {test_file} not found")
    
    return all(code == 0 for code in results)

def main():
    parser = argparse.ArgumentParser(description="Run CitiBike backend tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", "-c", action="store_true", help="Generate coverage report")
    parser.add_argument("--markers", "-m", help="Run tests with specific markers")
    parser.add_argument("--legacy", action="store_true", help="Run legacy test scripts")
    parser.add_argument("--all", action="store_true", help="Run all tests (pytest + legacy)")
    
    args = parser.parse_args()
    
    # Set up test environment
    setup_test_environment()
    
    print("CitiBike Backend Test Runner")
    print("=" * 40)
    
    success = True
    
    if args.legacy or args.all:
        print("\n1. Running legacy tests...")
        legacy_success = run_legacy_tests()
        if not legacy_success:
            success = False
            print("❌ Legacy tests failed")
        else:
            print("✅ Legacy tests passed")
    
    if not args.legacy or args.all:
        print("\n2. Running pytest tests...")
        pytest_success = run_pytest_tests(
            verbose=args.verbose,
            coverage=args.coverage,
            markers=args.markers
        )
        if pytest_success != 0:
            success = False
            print("❌ Pytest tests failed")
        else:
            print("✅ Pytest tests passed")
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 All tests passed!")
        return 0
    else:
        print("💥 Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
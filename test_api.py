#!/usr/bin/env python3
"""
Simple test script to verify FastAPI endpoints
"""
import requests
import json
import time

def test_api():
    base_url = "http://localhost:8000"
    
    print("Testing CitiBike Probability API...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/api/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()
    except Exception as e:
        print(f"   Error: {e}")
        print()
    
    # Test root endpoint
    try:
        print("2. Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()
    except Exception as e:
        print(f"   Error: {e}")
        print()
    
    # Test stations endpoint
    try:
        print("3. Testing stations endpoint...")
        response = requests.get(f"{base_url}/api/stations")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()
    except Exception as e:
        print(f"   Error: {e}")
        print()
    
    # Test probability endpoint
    try:
        print("4. Testing probability endpoint...")
        data = {
            "home_station_id": "test_station_1",
            "riding_frequency": 5,
            "time_pattern": "weekday"
        }
        response = requests.post(f"{base_url}/api/probability", json=data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print()
    except Exception as e:
        print(f"   Error: {e}")
        print()

if __name__ == "__main__":
    test_api() 
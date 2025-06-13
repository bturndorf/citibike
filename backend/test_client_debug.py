#!/usr/bin/env python3
"""
Debug script to test TestClient configuration
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from fastapi.testclient import TestClient
    print("✓ TestClient imported successfully")
    
    from main import app
    print("✓ FastAPI app imported successfully")
    
    # Create test client with correct syntax
    client = TestClient(app=app)
    print("✓ TestClient created successfully")
    
    # Test health endpoint
    response = client.get('/api/health')
    print(f"✓ Health endpoint test: Status {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n🎉 TestClient configuration is working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 
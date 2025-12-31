"""
Test script for PeakMapPH API
Run this after starting the server to verify all endpoints
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the root endpoint"""
    print("\n" + "="*60)
    print("Testing: Health Check (GET /)")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_update_bus():
    """Test updating bus status"""
    print("\n" + "="*60)
    print("Testing: Update Bus (POST /update)")
    print("="*60)
    
    test_data = [
        {
            "bus_id": "BUS001",
            "count": 35,
            "lat": 14.6091,
            "lng": 121.0223,
            "route": "EDSA",
            "destination": "Cubao"
        },
        {
            "bus_id": "BUS002",
            "count": 42,
            "lat": 14.6850,
            "lng": 121.0794,
            "route": "Commonwealth",
            "destination": "Quezon City"
        },
        {
            "bus_id": "BUS003",
            "count": 15,
            "lat": 14.6344,
            "lng": 121.0712,
            "route": "Katipunan",
            "destination": "Antipolo"
        }
    ]
    
    for data in test_data:
        response = requests.post(f"{BASE_URL}/update", json=data)
        print(f"\nBus: {data['bus_id']}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return True

def test_get_buses():
    """Test getting all buses"""
    print("\n" + "="*60)
    print("Testing: Get All Buses (GET /buses)")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/buses")
    print(f"Status Code: {response.status_code}")
    buses = response.json()
    print(f"Total Buses: {len(buses)}")
    print(f"Response: {json.dumps(buses, indent=2)}")
    return response.status_code == 200

def test_get_specific_bus():
    """Test getting specific bus"""
    print("\n" + "="*60)
    print("Testing: Get Specific Bus (GET /bus/BUS001)")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/bus/BUS001")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_stats():
    """Test getting system statistics"""
    print("\n" + "="*60)
    print("Testing: Get Statistics (GET /stats)")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_delete_bus():
    """Test deleting a bus"""
    print("\n" + "="*60)
    print("Testing: Delete Bus (DELETE /bus/BUS003)")
    print("="*60)
    
    response = requests.delete(f"{BASE_URL}/bus/BUS003")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def run_all_tests():
    """Run all API tests"""
    print("\n" + "🚌 PeakMapPH API Test Suite")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "Health Check": test_health_check(),
        "Update Bus": test_update_bus(),
        "Get All Buses": test_get_buses(),
        "Get Specific Bus": test_get_specific_bus(),
        "Get Statistics": test_get_stats(),
        "Delete Bus": test_delete_bus(),
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server!")
        print("Make sure the backend is running: python main.py")
        print("Server should be at: http://localhost:8000\n")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")

"""
Quick API test script for Integraty backend
"""
import requests
import json
import time

BASE_URL = "http://localhost:8080"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_create_session():
    """Test creating a session"""
    print("Creating a new session...")
    data = {
        "user_id": "test-user-123",
        "session_name": "Test Monitoring Session",
        "session_type": "exam",
        "screenshot_interval": 30,
        "screenshot_quality": 85
    }
    response = requests.post(f"{BASE_URL}/api/v1/sessions/", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    print()
    return result.get("session_id")

def test_start_session(session_id):
    """Test starting a session"""
    print(f"Starting session {session_id}...")
    response = requests.post(f"{BASE_URL}/api/v1/sessions/{session_id}/start")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_get_session(session_id):
    """Test getting session details"""
    print(f"Getting session details for {session_id}...")
    response = requests.get(f"{BASE_URL}/api/v1/sessions/{session_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_complete_session(session_id):
    """Test completing a session"""
    print(f"Completing session {session_id}...")
    response = requests.post(f"{BASE_URL}/api/v1/sessions/{session_id}/complete")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    print("="*60)
    print("INTEGRATY API TEST")
    print("="*60)
    print()

    try:
        # Test health
        test_health()

        # Create session
        session_id = test_create_session()

        if session_id:
            # Start session
            test_start_session(session_id)

            # Wait a bit
            print("Waiting 10 seconds for monitoring...")
            time.sleep(10)

            # Get session details
            test_get_session(session_id)

            # Complete session
            test_complete_session(session_id)

        print("="*60)
        print("ALL TESTS COMPLETED!")
        print("="*60)

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server")
        print("Make sure the server is running: python -m integraty.main")
    except Exception as e:
        print(f"ERROR: {e}")

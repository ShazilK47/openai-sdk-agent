"""
Test script for the FastAPI endpoints.
Quick way to test all our API functionality.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_tools():
    """Test tools endpoint"""
    print("🛠️ Testing Tools Endpoint...")
    response = requests.get(f"{BASE_URL}/api/tools/available")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {data['total_count']} tools:")
    for tool in data['tools']:
        print(f"  - {tool['name']}: {tool['description']}")
    print()

def test_tool_execution():
    """Test tool execution"""
    print("⚡ Testing Tool Execution...")
    
    # Test calculator
    print("Testing Calculator:")
    response = requests.post(
        f"{BASE_URL}/api/tools/execute",
        json={
            "tool_name": "calculate",
            "parameters": {"expression": "10 * 5 + 2"}
        }
    )
    result = response.json()
    print(f"  Result: {result['result']}")
    print(f"  Time: {result['execution_time']:.3f}s")
    print()

def test_chat():
    """Test chat endpoint"""
    print("💬 Testing Chat Endpoint...")
    response = requests.post(
        f"{BASE_URL}/api/chat/message",
        json={
            "message": "Calculate 15 * 3 for me",
            "conversation_id": "test_conv_001"
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {result['response']}")
        print(f"Tools used: {len(result['tool_usage'])}")
        for tool in result['tool_usage']:
            print(f"  - {tool['tool_name']}: {tool['status']}")
    else:
        print(f"Error: {response.status_code}")
        print(f"Details: {response.text}")
    print()

if __name__ == "__main__":
    print("🚀 Testing FastAPI AI Agent Endpoints\n")
    
    try:
        test_health()
        test_tools()
        test_tool_execution()
        test_chat()
        
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

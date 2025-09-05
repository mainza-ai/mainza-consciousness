#!/usr/bin/env python3
"""
Backend-Frontend Integration Test
Tests all API endpoints that the frontend calls to ensure they're working
"""
import requests
import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"

def test_endpoint(method: str, endpoint: str, data: Dict[Any, Any] = None, files: Dict[str, Any] = None) -> Dict[str, Any]:
    """Test a single endpoint and return results"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            if files:
                response = requests.post(url, files=files, timeout=10)
            else:
                response = requests.post(url, json=data, timeout=10)
        else:
            return {"status": "error", "message": f"Unsupported method: {method}"}
        
        return {
            "status": "success" if response.status_code < 400 else "error",
            "status_code": response.status_code,
            "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text[:200]
        }
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}

def main():
    """Test all frontend-backend integration points"""
    
    print("🧪 Testing Backend-Frontend Integration")
    print("=" * 50)
    
    # Test cases based on frontend API calls
    test_cases = [
        # Core consciousness endpoints
        ("GET", "/consciousness/state", None, "Consciousness state fetching"),
        ("POST", "/consciousness/reflect", {}, "Self-reflection trigger"),
        ("GET", "/consciousness/metrics", None, "Consciousness metrics"),
        
        # Chat and routing
        ("POST", "/agent/router/chat", {"query": "Hello, how are you?", "user_id": "test-user"}, "Router chat"),
        
        # Needs analysis
        ("POST", "/mainza/analyze_needs", {}, "Needs analysis"),
        
        # Recommendations
        ("GET", "/recommendations/next_steps?user_id=test-user", None, "Recommendations"),
        
        # TTS/STT endpoints
        ("GET", "/tts/voices", None, "TTS voices list"),
        ("POST", "/tts/synthesize", {"text": "Hello world", "language": "en"}, "TTS synthesis"),
        
        # LiveKit integration
        ("POST", "/livekit/token", {"user": "test-user", "room": "test-room"}, "LiveKit token"),
        
        # Health checks
        ("GET", "/health", None, "Health check"),
        ("GET", "/neo4j/ping", None, "Neo4j connection"),
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for method, endpoint, data, description in test_cases:
        print(f"\n🔍 Testing: {description}")
        print(f"   {method} {endpoint}")
        
        result = test_endpoint(method, endpoint, data)
        results.append({
            "endpoint": endpoint,
            "method": method,
            "description": description,
            "result": result
        })
        
        if result["status"] == "success":
            print(f"   ✅ PASS - Status: {result['status_code']}")
            passed += 1
        else:
            print(f"   ❌ FAIL - {result.get('message', 'Unknown error')}")
            if 'status_code' in result:
                print(f"      Status: {result['status_code']}")
            failed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 INTEGRATION TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed / (passed + failed) * 100):.1f}%")
    
    # Detailed results for failures
    if failed > 0:
        print("\n🔍 FAILURE DETAILS:")
        print("-" * 30)
        for test in results:
            if test["result"]["status"] == "error":
                print(f"\n❌ {test['description']}")
                print(f"   Endpoint: {test['method']} {test['endpoint']}")
                print(f"   Error: {test['result'].get('message', 'Unknown')}")
                if 'response' in test['result']:
                    print(f"   Response: {test['result']['response']}")
    
    # Success details
    if passed > 0:
        print(f"\n✅ SUCCESSFUL ENDPOINTS ({passed}):")
        print("-" * 30)
        for test in results:
            if test["result"]["status"] == "success":
                print(f"   ✅ {test['description']} - {test['method']} {test['endpoint']}")
    
    print(f"\n🎯 Integration Status: {'HEALTHY' if failed == 0 else 'NEEDS ATTENTION'}")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
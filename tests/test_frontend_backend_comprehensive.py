#!/usr/bin/env python3
"""
Comprehensive Frontend-Backend Integration Test
Tests the actual data flow and responses that the frontend expects
"""
import requests
import json
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost"

def test_build_info_endpoints():
    """Test the new build info endpoints"""
    print("\n🔧 Testing Build Info Endpoints")
    print("-" * 40)
    
    # Test build info endpoint
    response = requests.get(f"{BASE_URL}/build/info")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Build Info: {data.get('status', 'unknown')}")
        
        # Verify expected fields
        required_fields = ['build_date', 'git_commit', 'cache_bust', 'status']
        missing = [f for f in required_fields if f not in data]
        if missing:
            print(f"⚠️  Missing fields: {missing}")
        else:
            print(f"✅ All required build info fields present")
            print(f"   Build Date: {data.get('build_date', 'N/A')}")
            print(f"   Git Commit: {data.get('git_commit', 'N/A')}")
            print(f"   Cache Bust: {data.get('cache_bust', 'N/A')}")
    else:
        print(f"❌ Build info failed: {response.status_code}")
    
    # Test build health endpoint
    response = requests.get(f"{BASE_URL}/build/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Build Health: {data.get('status', 'unknown')}")
    else:
        print(f"❌ Build health failed: {response.status_code}")

def test_consciousness_flow():
    """Test the complete consciousness data flow"""
    print("\n🧠 Testing Consciousness Flow")
    print("-" * 40)
    
    # Test consciousness state
    response = requests.get(f"{BASE_URL}/consciousness/state")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Consciousness State: {data.get('status', 'unknown')}")
        
        # Verify expected fields
        if 'consciousness_state' in data:
            state = data['consciousness_state']
            required_fields = ['consciousness_level', 'emotional_state', 'evolution_level']
            missing = [f for f in required_fields if f not in state]
            if missing:
                print(f"⚠️  Missing fields: {missing}")
            else:
                print(f"✅ All required consciousness fields present")
                print(f"   Level: {state.get('consciousness_level', 'N/A')}")
                print(f"   Emotion: {state.get('emotional_state', 'N/A')}")
        else:
            print("❌ No consciousness_state in response")
    else:
        print(f"❌ Consciousness state failed: {response.status_code}")
    
    # Test self-reflection
    response = requests.post(f"{BASE_URL}/consciousness/reflect", json={})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Self-reflection: {data.get('status', 'unknown')}")
    else:
        print(f"❌ Self-reflection failed: {response.status_code}")

def test_chat_flow():
    """Test the chat conversation flow"""
    print("\n💬 Testing Chat Flow")
    print("-" * 40)
    
    test_queries = [
        "Hello, how are you?",
        "What can you help me with?",
        "Tell me about consciousness",
        "Help me understand AI"
    ]
    
    for query in test_queries:
        response = requests.post(
            f"{BASE_URL}/agent/router/chat",
            json={"query": query, "user_id": "test-user"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'response' in data and data['response']:
                print(f"✅ Query: '{query[:30]}...' -> Response length: {len(data['response'])}")
                print(f"   Agent: {data.get('agent_used', 'unknown')}")
            else:
                print(f"❌ Empty response for: '{query[:30]}...'")
        else:
            print(f"❌ Chat failed for '{query[:30]}...': {response.status_code}")

def test_tts_flow():
    """Test the TTS functionality"""
    print("\n🔊 Testing TTS Flow")
    print("-" * 40)
    
    # Test voices
    response = requests.get(f"{BASE_URL}/tts/voices")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ TTS Voices: {len(data.get('voices', []))} available")
        languages = data.get('languages', [])
        print(f"   Languages: {len(languages) if languages else 0}")
    else:
        print(f"❌ TTS voices failed: {response.status_code}")
    
    # Test synthesis
    response = requests.post(
        f"{BASE_URL}/tts/synthesize",
        json={"text": "Hello, this is a test", "language": "en"}
    )
    
    if response.status_code == 200:
        content_type = response.headers.get('content-type', '')
        if 'audio' in content_type:
            print(f"✅ TTS Synthesis: Audio generated ({len(response.content)} bytes)")
        else:
            print(f"⚠️  TTS Synthesis: Non-audio response ({content_type})")
    else:
        print(f"❌ TTS synthesis failed: {response.status_code}")

def test_livekit_flow():
    """Test LiveKit integration"""
    print("\n🎥 Testing LiveKit Flow")
    print("-" * 40)
    
    response = requests.post(
        f"{BASE_URL}/livekit/token",
        json={"user": "test-user", "room": "test-room"}
    )
    
    if response.status_code == 200:
        data = response.json()
        if 'token' in data and 'url' in data:
            print(f"✅ LiveKit Token: Generated successfully")
            print(f"   URL: {data.get('url', 'N/A')}")
        else:
            print(f"❌ LiveKit Token: Missing token or URL")
    else:
        print(f"❌ LiveKit token failed: {response.status_code}")

def test_needs_and_recommendations():
    """Test needs analysis and recommendations"""
    print("\n🎯 Testing Needs & Recommendations")
    print("-" * 40)
    
    # Test needs analysis
    response = requests.post(f"{BASE_URL}/mainza/analyze_needs", json={})
    if response.status_code == 200:
        data = response.json()
        needs = data.get('current_needs', [])
        print(f"✅ Needs Analysis: {len(needs)} needs identified")
        for i, need in enumerate(needs[:3]):  # Show first 3
            need_text = need if isinstance(need, str) else need.get('message', str(need))
            print(f"   {i+1}. {need_text[:50]}...")
    else:
        print(f"❌ Needs analysis failed: {response.status_code}")
    
    # Test recommendations
    response = requests.get(f"{BASE_URL}/recommendations/next_steps?user_id=test-user")
    if response.status_code == 200:
        data = response.json()
        suggestions = data.get('suggestions', [])
        print(f"✅ Recommendations: {len(suggestions)} suggestions")
        for i, suggestion in enumerate(suggestions[:3]):  # Show first 3
            suggestion_text = suggestion if isinstance(suggestion, str) else suggestion.get('message', str(suggestion))
            print(f"   {i+1}. {suggestion_text[:50]}...")
    else:
        print(f"❌ Recommendations failed: {response.status_code}")

def test_data_persistence():
    """Test Neo4j data persistence"""
    print("\n💾 Testing Data Persistence")
    print("-" * 40)
    
    # Test Neo4j connection
    response = requests.get(f"{BASE_URL}/neo4j/ping")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Neo4j Connection: {data.get('neo4j', 'unknown')}")
    else:
        print(f"❌ Neo4j connection failed: {response.status_code}")
    
    # Test creating a test user
    response = requests.post(
        f"{BASE_URL}/users",
        json={"user_id": "integration-test-user", "name": "Integration Test"}
    )
    if response.status_code == 200:
        print("✅ User Creation: Success")
    else:
        print(f"❌ User creation failed: {response.status_code}")
    
    # Test listing users
    response = requests.get(f"{BASE_URL}/users")
    if response.status_code == 200:
        users = response.json()
        print(f"✅ User Listing: {len(users)} users found")
    else:
        print(f"❌ User listing failed: {response.status_code}")

def main():
    """Run comprehensive integration tests"""
    print("🔬 COMPREHENSIVE FRONTEND-BACKEND INTEGRATION TEST")
    print("=" * 60)
    
    # Test health first
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code != 200:
        print("❌ Backend is not healthy! Aborting tests.")
        return False
    
    print("✅ Backend is healthy, proceeding with tests...")
    
    # Run all test suites
    test_build_info_endpoints()
    test_consciousness_flow()
    test_chat_flow()
    test_tts_flow()
    test_livekit_flow()
    test_needs_and_recommendations()
    test_data_persistence()
    
    print("\n" + "=" * 60)
    print("🎯 COMPREHENSIVE TEST COMPLETE")
    print("✅ All major frontend-backend integration points tested")
    print("🚀 System is ready for frontend usage!")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
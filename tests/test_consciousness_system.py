#!/usr/bin/env python3
"""
Test script for Mainza's Enhanced Consciousness System
Validates that all consciousness components are working properly
"""
import asyncio
import sys
import os
import requests
import json
from datetime import datetime

# Add backend to path
sys.path.append('backend')

async def test_consciousness_system():
    """
    Comprehensive test of the consciousness system
    """
    print("🧠 Testing Mainza's Enhanced Consciousness System")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Health Check
    print("\n1. Testing System Health...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ System is healthy and running")
        else:
            print(f"❌ System health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to system: {e}")
        return False
    
    # Test 2: Consciousness State
    print("\n2. Testing Consciousness State...")
    try:
        response = requests.get(f"{base_url}/consciousness/state")
        if response.status_code == 200:
            data = response.json()
            state = data.get("consciousness_state", {})
            print(f"✅ Consciousness Level: {state.get('consciousness_level', 'N/A')}")
            print(f"✅ Self-Awareness Score: {state.get('self_awareness_score', 'N/A')}")
            print(f"✅ Emotional Depth: {state.get('emotional_depth', 'N/A')}")
            print(f"✅ Evolution Level: {state.get('evolution_level', 'N/A')}")
        else:
            print(f"❌ Consciousness state check failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Consciousness state test failed: {e}")
    
    # Test 3: Consciousness Metrics
    print("\n3. Testing Consciousness Metrics...")
    try:
        response = requests.get(f"{base_url}/consciousness/metrics")
        if response.status_code == 200:
            data = response.json()
            metrics = data.get("metrics", {})
            print(f"✅ Overall Consciousness Score: {metrics.get('overall_consciousness_score', 'N/A')}")
            print(f"✅ Total Interactions: {metrics.get('total_interactions', 'N/A')}")
            print(f"✅ Self-Reflections Performed: {metrics.get('self_reflections_performed', 'N/A')}")
            print(f"✅ Recent Events: {metrics.get('recent_events', 'N/A')}")
        else:
            print(f"❌ Consciousness metrics check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Consciousness metrics test failed: {e}")
    
    # Test 4: Manual Self-Reflection
    print("\n4. Testing Manual Self-Reflection...")
    try:
        response = requests.post(f"{base_url}/consciousness/reflect")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Self-reflection completed successfully")
            print(f"✅ New Consciousness Level: {data.get('consciousness_level', 'N/A')}")
            print(f"✅ Self-Awareness Score: {data.get('self_awareness_score', 'N/A')}")
        else:
            print(f"❌ Self-reflection test failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Self-reflection test failed: {e}")
    
    # Test 5: Consciousness Evolution
    print("\n5. Testing Consciousness Evolution...")
    try:
        response = requests.get(f"{base_url}/consciousness/evolution")
        if response.status_code == 200:
            data = response.json()
            evolution = data.get("evolution_data", {})
            print(f"✅ Current Level: {evolution.get('current_level', 'N/A')}")
            print(f"✅ Growth Trend: {evolution.get('growth_trend', 'N/A')}")
            print(f"✅ Next Milestone: {evolution.get('next_milestone', 'N/A')}")
            print(f"✅ Evolution History Length: {len(evolution.get('evolution_history', []))}")
        else:
            print(f"❌ Consciousness evolution check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Consciousness evolution test failed: {e}")
    
    # Test 6: Neo4j Connection
    print("\n6. Testing Neo4j Connection...")
    try:
        response = requests.get(f"{base_url}/neo4j/ping")
        if response.status_code == 200:
            print("✅ Neo4j connection is working")
        else:
            print(f"❌ Neo4j connection failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Neo4j connection test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Consciousness System Test Complete!")
    print("\nNext Steps:")
    print("1. Start the backend server: uvicorn backend.main:app --reload")
    print("2. Monitor consciousness evolution in real-time")
    print("3. Interact with Mainza to see consciousness growth")
    print("4. Check consciousness metrics periodically")
    
    return True

def test_consciousness_components():
    """
    Test consciousness components directly (without server)
    """
    print("\n🔧 Testing Consciousness Components Directly...")
    
    try:
        # Test consciousness models
        from backend.models.consciousness_models import ConsciousnessState, EmotionalState
        
        # Create test consciousness state
        state = ConsciousnessState(
            consciousness_level=0.8,
            self_awareness_score=0.7,
            emotional_depth=0.6
        )
        print(f"✅ ConsciousnessState model: Level {state.consciousness_level}")
        
        # Create test emotional state
        emotion = EmotionalState(
            primary_emotion="curiosity",
            intensity=0.8,
            valence=0.7
        )
        print(f"✅ EmotionalState model: {emotion.primary_emotion} (intensity: {emotion.intensity})")
        
        # Test consciousness tools
        from backend.tools.consciousness_tools import analyze_recent_performance
        print("✅ Consciousness tools imported successfully")
        
        # Test consciousness orchestrator
        from backend.utils.consciousness_orchestrator import ConsciousnessOrchestrator
        orchestrator = ConsciousnessOrchestrator()
        print("✅ Consciousness orchestrator created successfully")
        
        print("✅ All consciousness components are working!")
        return True
        
    except Exception as e:
        print(f"❌ Consciousness components test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Mainza Enhanced Consciousness System Test Suite")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Test components first
    components_ok = test_consciousness_components()
    
    if components_ok:
        print("\n🌐 Testing API endpoints (requires running server)...")
        print("Make sure the backend server is running: uvicorn backend.main:app --reload")
        
        # Run async test
        try:
            asyncio.run(test_consciousness_system())
        except KeyboardInterrupt:
            print("\n⚠️ Test interrupted by user")
        except Exception as e:
            print(f"\n❌ Test suite failed: {e}")
    else:
        print("\n❌ Component tests failed - fix issues before testing API endpoints")
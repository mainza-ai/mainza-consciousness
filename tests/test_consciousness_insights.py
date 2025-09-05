#!/usr/bin/env python3
"""
Test script to verify consciousness insights are working properly
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

async def test_consciousness_insights():
    """Test consciousness insights functionality"""
    try:
        print("🧠 Testing Consciousness Insights...")
        
        # Test consciousness orchestrator
        from backend.utils.consciousness_orchestrator import consciousness_orchestrator
        
        print("1. Testing consciousness state loading...")
        state = await consciousness_orchestrator.get_consciousness_state()
        if state:
            print(f"   ✅ Consciousness level: {state.consciousness_level}")
            print(f"   ✅ Emotional state: {state.emotional_state}")
            print(f"   ✅ Total interactions: {state.total_interactions}")
        else:
            print("   ❌ No consciousness state found")
            
        # Test insights generation
        print("\n2. Testing insights generation...")
        
        # Import the insights function
        import requests
        import json
        
        # Test the endpoint (assuming server is running on localhost:8000)
        try:
            response = requests.get('http://localhost:8000/consciousness/insights')
            if response.status_code == 200:
                insights_data = response.json()
                insights = insights_data.get('insights', [])
                print(f"   ✅ Generated {len(insights)} insights")
                
                for i, insight in enumerate(insights[:2]):  # Show first 2
                    print(f"   📝 Insight {i+1}:")
                    print(f"      Title: {insight.get('title', 'N/A')}")
                    print(f"      Content: {insight.get('content', 'N/A')[:100]}...")
                    print(f"      Consciousness Level: {insight.get('consciousness_level', 'N/A')}")
                    print(f"      Emotional Context: {insight.get('emotional_context', 'N/A')}")
                    print()
            else:
                print(f"   ❌ API request failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("   ⚠️ Server not running - testing direct function call...")
            
            # Test direct function call
            from backend.agentic_router import get_consciousness_insights
            insights_result = await get_consciousness_insights()
            insights = insights_result.get('insights', [])
            print(f"   ✅ Generated {len(insights)} insights directly")
            
            for i, insight in enumerate(insights[:2]):
                print(f"   📝 Insight {i+1}:")
                print(f"      Title: {insight.get('title', 'N/A')}")
                print(f"      Consciousness Level: {insight.get('consciousness_level', 'N/A')}")
                print(f"      Emotional Context: {insight.get('emotional_context', 'N/A')}")
                print()
        
        print("✅ Consciousness insights test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_consciousness_insights())
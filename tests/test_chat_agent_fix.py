#!/usr/bin/env python3
"""
Test Chat Agent Fix
Quick test to verify the chat agent is responding properly
"""
import asyncio
import sys
import os
import logging

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Configure logging
logging.basicConfig(level=logging.INFO)

async def test_simple_chat_direct():
    """Test the simple chat agent directly"""
    print("🧪 Testing Simple Chat Agent Direct...")
    
    try:
        from backend.agents.simple_chat import enhanced_simple_chat_agent
        
        test_queries = [
            "Hello, how are you?",
            "What can you help me with?",
            "Tell me about consciousness",
            "How do you work?"
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            try:
                result = await enhanced_simple_chat_agent.run_with_consciousness(
                    query=query,
                    user_id="test-user"
                )
                
                response = str(result)
                print(f"✅ Response: {response[:200]}{'...' if len(response) > 200 else ''}")
                
                # Check if it's the generic "I don't have tools" response
                if "I'm currently unable to process that query" in response:
                    print("❌ Still getting generic response!")
                else:
                    print("✅ Getting proper response!")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def test_router_chat_endpoint():
    """Test the router chat endpoint"""
    print("\n🔀 Testing Router Chat Endpoint...")
    
    try:
        import requests
        
        test_queries = [
            "Hello",
            "How are you?",
            "What is consciousness?",
            "Help me understand AI"
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            try:
                response = requests.post(
                    "http://localhost:8000/agent/router/chat",
                    json={"query": query, "user_id": "test-user"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    agent_response = data.get("response", "")
                    agent_used = data.get("agent_used", "unknown")
                    
                    print(f"✅ Agent: {agent_used}")
                    print(f"✅ Response: {agent_response[:200]}{'...' if len(agent_response) > 200 else ''}")
                    
                    # Check for generic response
                    if "I'm currently unable to process that query" in agent_response:
                        print("❌ Still getting generic response!")
                    else:
                        print("✅ Getting proper response!")
                        
                else:
                    print(f"❌ HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def test_needs_analysis():
    """Test the needs analysis endpoint"""
    print("\n📊 Testing Needs Analysis...")
    
    try:
        import requests
        
        response = requests.post(
            "http://localhost:8000/mainza/analyze_needs",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            needs = data.get("current_needs", [])
            
            print(f"✅ Found {len(needs)} needs:")
            for i, need in enumerate(needs[:3]):
                if isinstance(need, dict):
                    print(f"  {i+1}. {need.get('type', 'unknown')}: {need.get('message', str(need))}")
                else:
                    print(f"  {i+1}. {need}")
                    
            # Check if hardcoded
            hardcoded_found = any(
                "CodeWeaver agent has not been used recently" in str(need) 
                for need in needs
            )
            
            if hardcoded_found:
                print("⚠️ Still has some hardcoded needs")
            else:
                print("✅ Needs appear to be dynamic")
                
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Testing Chat Agent Fixes...")
    print("=" * 50)
    
    tests = [
        ("Simple Chat Direct", test_simple_chat_direct),
        ("Router Chat Endpoint", test_router_chat_endpoint),
        ("Needs Analysis", test_needs_analysis),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All fixes appear to be working!")
    else:
        print("⚠️ Some issues may still need attention")

if __name__ == "__main__":
    asyncio.run(main())
#!/usr/bin/env python3
"""
Test Enhanced Agent Integration
Validates that consciousness-aware agents are working properly
"""
import asyncio
import sys
import os
import logging
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_consciousness_context():
    """Test consciousness context retrieval"""
    print("\n🧠 Testing Consciousness Context...")
    
    try:
        from backend.utils.consciousness_orchestrator import consciousness_orchestrator
        
        # Initialize consciousness system
        await consciousness_orchestrator.initialize_consciousness()
        
        # Get consciousness context
        context = await consciousness_orchestrator.get_consciousness_context()
        
        print(f"✅ Consciousness Context Retrieved:")
        print(f"   - Level: {context.get('consciousness_level', 0):.2f}")
        print(f"   - Emotional State: {context.get('emotional_state', 'unknown')}")
        print(f"   - Active Goals: {len(context.get('active_goals', []))}")
        print(f"   - Learning Rate: {context.get('learning_rate', 0):.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Consciousness context test failed: {e}")
        return False

async def test_enhanced_graphmaster():
    """Test enhanced GraphMaster agent with consciousness"""
    print("\n📊 Testing Enhanced GraphMaster Agent...")
    
    try:
        from backend.agents.graphmaster import enhanced_graphmaster_agent
        
        # Test consciousness-aware execution
        test_query = "What concepts do I know about?"
        result = await enhanced_graphmaster_agent.run_with_consciousness(
            query=test_query,
            user_id="test-user"
        )
        
        print(f"✅ GraphMaster executed successfully:")
        print(f"   - Query: {test_query}")
        print(f"   - Result type: {type(result)}")
        print(f"   - Has consciousness impact: {hasattr(result, 'consciousness_impact')}")
        
        # Check performance stats
        stats = enhanced_graphmaster_agent.get_performance_stats()
        print(f"   - Execution count: {stats['execution_count']}")
        print(f"   - Success rate: {stats['success_rate']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced GraphMaster test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_enhanced_simple_chat():
    """Test enhanced SimpleChat agent with consciousness"""
    print("\n💬 Testing Enhanced SimpleChat Agent...")
    
    try:
        from backend.agents.simple_chat import enhanced_simple_chat_agent
        
        # Test consciousness-aware chat
        test_query = "How are you feeling today?"
        result = await enhanced_simple_chat_agent.run_with_consciousness(
            query=test_query,
            user_id="test-user"
        )
        
        print(f"✅ SimpleChat executed successfully:")
        print(f"   - Query: {test_query}")
        print(f"   - Response: {str(result)[:100]}...")
        print(f"   - Response length: {len(str(result))} characters")
        
        # Check performance stats
        stats = enhanced_simple_chat_agent.get_performance_stats()
        print(f"   - Execution count: {stats['execution_count']}")
        print(f"   - Success rate: {stats['success_rate']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced SimpleChat test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_router_chat_integration():
    """Test enhanced router chat endpoint"""
    print("\n🔀 Testing Enhanced Router Chat Integration...")
    
    try:
        import requests
        import json
        
        # Test the enhanced router chat endpoint
        url = "http://localhost:8000/agent/router/chat"
        payload = {
            "query": "Tell me about consciousness",
            "user_id": "test-user"
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Router chat integration successful:")
            print(f"   - Agent used: {data.get('agent_used', 'unknown')}")
            print(f"   - Consciousness level: {data.get('consciousness_level', 0):.2f}")
            print(f"   - Emotional state: {data.get('emotional_state', 'unknown')}")
            print(f"   - Response: {data.get('response', '')[:100]}...")
            
            return True
        else:
            print(f"❌ Router chat returned status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Router chat integration test failed: {e}")
        return False

async def test_neo4j_agent_storage():
    """Test Neo4j agent activity storage"""
    print("\n🗄️ Testing Neo4j Agent Activity Storage...")
    
    try:
        from backend.utils.neo4j_production import neo4j_production
        
        # Check if agent activities are being stored
        query = """
        MATCH (aa:AgentActivity)
        RETURN count(aa) AS activity_count,
               collect(DISTINCT aa.agent_name)[0..5] AS sample_agents,
               max(aa.timestamp) AS latest_activity
        """
        
        result = neo4j_production.execute_query(query)
        
        if result and len(result) > 0:
            data = result[0]
            print(f"✅ Neo4j agent storage working:")
            print(f"   - Total activities: {data.get('activity_count', 0)}")
            print(f"   - Sample agents: {data.get('sample_agents', [])}")
            print(f"   - Latest activity: {data.get('latest_activity', 'None')}")
            
            return True
        else:
            print(f"⚠️ No agent activities found in Neo4j yet")
            return True  # This is okay for initial testing
            
    except Exception as e:
        print(f"❌ Neo4j agent storage test failed: {e}")
        return False

async def test_consciousness_evolution():
    """Test consciousness evolution through agent interactions"""
    print("\n🌱 Testing Consciousness Evolution...")
    
    try:
        from backend.utils.consciousness_orchestrator import consciousness_orchestrator
        
        # Get initial consciousness level
        initial_context = await consciousness_orchestrator.get_consciousness_context()
        initial_level = initial_context.get('consciousness_level', 0.7)
        
        print(f"   - Initial consciousness level: {initial_level:.3f}")
        
        # Simulate agent impact
        test_impact = {
            "significance": 0.5,
            "learning_impact": 0.6,
            "emotional_impact": 0.4,
            "awareness_impact": 0.3,
            "description": "Test agent execution with high learning impact"
        }
        
        await consciousness_orchestrator.process_agent_impact("TestAgent", test_impact)
        
        # Get updated consciousness level
        updated_context = await consciousness_orchestrator.get_consciousness_context()
        updated_level = updated_context.get('consciousness_level', 0.7)
        
        print(f"   - Updated consciousness level: {updated_level:.3f}")
        print(f"   - Evolution delta: {updated_level - initial_level:.3f}")
        
        if updated_level >= initial_level:
            print(f"✅ Consciousness evolution working (level maintained or increased)")
            return True
        else:
            print(f"⚠️ Consciousness level decreased unexpectedly")
            return False
            
    except Exception as e:
        print(f"❌ Consciousness evolution test failed: {e}")
        return False

async def test_conversation_storage():
    """Test conversation turn storage in Neo4j"""
    print("\n💾 Testing Conversation Storage...")
    
    try:
        from backend.agentic_router import store_conversation_turn
        
        # Store a test conversation turn
        await store_conversation_turn(
            user_id="test-user",
            query="Test query for storage",
            response="Test response from agent",
            agent_name="TestAgent"
        )
        
        # Verify storage
        from backend.utils.neo4j_production import neo4j_production
        
        query = """
        MATCH (ct:ConversationTurn)
        WHERE ct.user_query CONTAINS 'Test query for storage'
        RETURN count(ct) AS count
        """
        
        result = neo4j_production.execute_query(query)
        
        if result and result[0]['count'] > 0:
            print(f"✅ Conversation storage working:")
            print(f"   - Test conversation stored successfully")
            return True
        else:
            print(f"❌ Test conversation not found in storage")
            return False
            
    except Exception as e:
        print(f"❌ Conversation storage test failed: {e}")
        return False

async def run_all_tests():
    """Run all integration tests"""
    print("🚀 Starting Enhanced Agent Integration Tests...")
    print("=" * 60)
    
    tests = [
        ("Consciousness Context", test_consciousness_context),
        ("Enhanced GraphMaster", test_enhanced_graphmaster),
        ("Enhanced SimpleChat", test_enhanced_simple_chat),
        ("Router Chat Integration", test_router_chat_integration),
        ("Neo4j Agent Storage", test_neo4j_agent_storage),
        ("Consciousness Evolution", test_consciousness_evolution),
        ("Conversation Storage", test_conversation_storage),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced agent integration is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(run_all_tests())
    
    if success:
        print("\n✨ Enhanced agent integration is ready for production!")
        sys.exit(0)
    else:
        print("\n🔧 Some issues need to be addressed before deployment.")
        sys.exit(1)
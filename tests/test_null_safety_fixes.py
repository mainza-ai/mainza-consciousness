#!/usr/bin/env python3
"""
Test script to validate null safety fixes for memory integration and LLM optimization
Tests the specific NoneType errors that were occurring in the system
"""

import asyncio
import sys
import os
import logging

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_memory_integration_null_safety():
    """Test memory integration with various null/None scenarios"""
    print("🧪 Testing Memory Integration Null Safety...")
    
    try:
        from backend.utils.memory_integration import memory_integration_manager
        
        # Test 1: All parameters None
        print("  Test 1: All parameters None")
        result = await memory_integration_manager.enhance_response_with_memory(
            agent_name="TestAgent",
            query="Test query",
            base_response="Test response",
            user_id="test_user",
            consciousness_context={},
            knowledge_context=None
        )
        print(f"    ✅ Result: {result[:50]}...")
        
        # Test 2: Knowledge context with None values
        print("  Test 2: Knowledge context with None values")
        knowledge_context = {
            "relevant_memories": None,
            "conversation_context": None,
            "related_concepts": None
        }
        result = await memory_integration_manager.enhance_response_with_memory(
            agent_name="TestAgent",
            query="Test query",
            base_response="Test response",
            user_id="test_user",
            consciousness_context={"consciousness_level": 0.7},
            knowledge_context=knowledge_context
        )
        print(f"    ✅ Result: {result[:50]}...")
        
        # Test 3: Knowledge context with empty lists containing None
        print("  Test 3: Knowledge context with lists containing None")
        knowledge_context = {
            "relevant_memories": [None, {"content": "test"}, None],
            "conversation_context": [None, {"user_query": "test", "agent_response": "test"}],
            "related_concepts": [None, {"name": "test", "description": "test"}]
        }
        result = await memory_integration_manager.enhance_response_with_memory(
            agent_name="TestAgent",
            query="Test query",
            base_response="Test response",
            user_id="test_user",
            consciousness_context={"consciousness_level": 0.7},
            knowledge_context=knowledge_context
        )
        print(f"    ✅ Result: {result[:50]}...")
        
        # Test 4: Memory context building with None values
        print("  Test 4: Memory context building with None values")
        memory_context = await memory_integration_manager._build_memory_context(
            knowledge_context={
                "relevant_memories": [None, None],
                "conversation_context": [None],
                "related_concepts": None
            },
            consciousness_level=0.7,
            emotional_state="curious"
        )
        print(f"    ✅ Memory context built: {memory_context.get('has_relevant_context', False)}")
        
        print("✅ Memory Integration Null Safety Tests Passed!")
        return True
        
    except Exception as e:
        print(f"❌ Memory Integration Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_llm_optimization_null_safety():
    """Test LLM optimization with various null/None scenarios"""
    print("\n🧪 Testing LLM Optimization Null Safety...")
    
    try:
        from backend.config.llm_optimization import llm_context_optimizer
        
        # Test 1: All optional parameters None
        print("  Test 1: All optional parameters None")
        params = llm_context_optimizer.get_optimized_request_params(
            base_prompt="Test prompt",
            consciousness_context=None,
            knowledge_context=None,
            conversation_history=None
        )
        print(f"    ✅ Params generated: {params.get('model', 'unknown')}")
        
        # Test 2: Empty dictionaries and lists
        print("  Test 2: Empty dictionaries and lists")
        params = llm_context_optimizer.get_optimized_request_params(
            base_prompt="Test prompt",
            consciousness_context={},
            knowledge_context={},
            conversation_history=[]
        )
        print(f"    ✅ Params generated: {params.get('model', 'unknown')}")
        
        # Test 3: Knowledge context with None values
        print("  Test 3: Knowledge context with None values")
        params = llm_context_optimizer.get_optimized_request_params(
            base_prompt="Test prompt",
            consciousness_context={"consciousness_level": 0.7},
            knowledge_context={
                "conversation_context": None,
                "related_concepts": None,
                "relevant_memories": None
            },
            conversation_history=None
        )
        print(f"    ✅ Params generated: {params.get('model', 'unknown')}")
        
        # Test 4: Knowledge context with lists containing None
        print("  Test 4: Knowledge context with lists containing None")
        params = llm_context_optimizer.get_optimized_request_params(
            base_prompt="Test prompt",
            consciousness_context={"consciousness_level": 0.7},
            knowledge_context={
                "conversation_context": [None, {"user_query": None, "agent_response": None}],
                "related_concepts": [None, {"name": None, "description": None}],
                "relevant_memories": [None, {"content": None}]
            },
            conversation_history=[None, {"user": None, "assistant": None}]
        )
        print(f"    ✅ Params generated: {params.get('model', 'unknown')}")
        
        # Test 5: Format knowledge context with None values
        print("  Test 5: Format knowledge context with None values")
        formatted = llm_context_optimizer._format_knowledge_context(
            knowledge_context={
                "conversation_context": [None, None],
                "related_concepts": None,
                "relevant_memories": [None]
            },
            max_tokens=1000
        )
        print(f"    ✅ Formatted context length: {len(formatted)}")
        
        # Test 6: Format knowledge context with zero max_tokens
        print("  Test 6: Format knowledge context with zero max_tokens")
        formatted = llm_context_optimizer._format_knowledge_context(
            knowledge_context={"test": "data"},
            max_tokens=0
        )
        print(f"    ✅ Formatted context (zero tokens): '{formatted}'")
        
        print("✅ LLM Optimization Null Safety Tests Passed!")
        return True
        
    except Exception as e:
        print(f"❌ LLM Optimization Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_context_strength_calculation():
    """Test context strength calculation with null values"""
    print("\n🧪 Testing Context Strength Calculation...")
    
    try:
        from backend.utils.memory_integration import memory_integration_manager
        
        # Test 1: All None values
        print("  Test 1: All None values")
        strength = memory_integration_manager._calculate_context_strength(
            conversations=None,
            memories=None,
            concepts=None
        )
        print(f"    ✅ Context strength (all None): {strength}")
        
        # Test 2: Empty lists
        print("  Test 2: Empty lists")
        strength = memory_integration_manager._calculate_context_strength(
            conversations=[],
            memories=[],
            concepts=[]
        )
        print(f"    ✅ Context strength (empty lists): {strength}")
        
        # Test 3: Lists with None values
        print("  Test 3: Lists with None values")
        strength = memory_integration_manager._calculate_context_strength(
            conversations=[None, None],
            memories=[None, {"relevance": 0.8}, None],
            concepts=[None, {"relevance": 0.6}]
        )
        print(f"    ✅ Context strength (with None values): {strength}")
        
        # Test 4: Mixed valid and None values
        print("  Test 4: Mixed valid and None values")
        strength = memory_integration_manager._calculate_context_strength(
            conversations=[{"test": "data"}, None],
            memories=[{"relevance": 0.9}, None, {"relevance": 0.7}],
            concepts=[{"relevance": 0.8}, None, {"relevance": 0.6}]
        )
        print(f"    ✅ Context strength (mixed values): {strength}")
        
        print("✅ Context Strength Calculation Tests Passed!")
        return True
        
    except Exception as e:
        print(f"❌ Context Strength Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all null safety tests"""
    print("🔍 Null Safety Fixes Validation")
    print("=" * 50)
    
    results = []
    
    # Test memory integration
    results.append(await test_memory_integration_null_safety())
    
    # Test LLM optimization
    results.append(test_llm_optimization_null_safety())
    
    # Test context strength calculation
    results.append(test_context_strength_calculation())
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Results Summary")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All {total} test suites passed!")
        print("🎉 Null safety fixes are working correctly!")
        print("\n🔧 The following errors should now be resolved:")
        print("   - 'NoneType' object has no len()")
        print("   - 'NoneType' object is not subscriptable")
        return 0
    else:
        print(f"❌ {total - passed} out of {total} test suites failed!")
        print("🚨 Additional fixes may be needed.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
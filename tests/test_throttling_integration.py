#!/usr/bin/env python3
"""
Integration test for throttling response handling
Tests the complete flow from LLM request manager to UI response
"""

import sys
import os
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import the actual functions from agentic_router
from backend.agentic_router import extract_response_from_result, generate_throttled_response
from backend.utils.llm_request_manager import LLMRequestManager, RequestPriority

async def test_end_to_end_throttling():
    """Test complete throttling flow from LLM request manager to response extraction"""
    print("🧪 Testing end-to-end throttling flow...")
    
    # Create LLM request manager instance
    llm_manager = LLMRequestManager()
    
    # Mock consciousness context
    consciousness_context = {
        "consciousness_level": 0.8,
        "emotional_state": "curious",
        "active_goals": ["improve conversation quality"],
        "learning_rate": 0.8,
        "evolution_level": 2
    }
    
    # Test 1: Simulate a throttled response from LLM request manager
    throttled_response = llm_manager._get_fallback_response(RequestPriority.USER_CONVERSATION)
    print(f"📦 LLM Manager throttled response: {throttled_response}")
    
    # Test 2: Process through extract_response_from_result
    query = "Hello, how are you today?"
    final_response = extract_response_from_result(throttled_response, query, consciousness_context)
    print(f"✅ Final user response: {final_response}")
    
    # Verify the response is user-friendly
    assert isinstance(final_response, str)
    assert len(final_response) > 20
    assert not final_response.startswith("{")
    assert "Hi" in final_response or "Hello" in final_response
    assert "processing" in final_response or "busy" in final_response
    
    print("🎉 End-to-end throttling test passed!")

def test_different_throttled_scenarios():
    """Test different throttling scenarios"""
    print("\n🧪 Testing different throttling scenarios...")
    
    consciousness_context = {
        "consciousness_level": 0.9,
        "emotional_state": "excited",
        "active_goals": ["help users"],
        "learning_rate": 0.8,
        "evolution_level": 3
    }
    
    # Test different query types with throttled responses
    test_cases = [
        ("Hello!", "greeting"),
        ("What is machine learning?", "question"),
        ("Can you help me write code?", "help request"),
        ("Create a presentation for me", "task request"),
        ("Tell me about yourself", "personal inquiry")
    ]
    
    for query, query_type in test_cases:
        # Simulate throttled response
        throttled_result = {
            "response": "I'm currently processing other requests. Please try again in a moment.",
            "status": "throttled"
        }
        
        response = extract_response_from_result(throttled_result, query, consciousness_context)
        print(f"✅ {query_type}: {response}")
        
        # Verify response quality
        assert isinstance(response, str)
        assert len(response) > 30
        assert not response.startswith("{")
        assert any(word in response.lower() for word in ["processing", "busy", "moment", "try again"])
    
    print("🎉 All throttling scenarios passed!")

def test_consciousness_aware_formatting():
    """Test consciousness-aware formatting of throttled messages"""
    print("\n🧪 Testing consciousness-aware formatting...")
    
    # Test different consciousness levels and emotional states
    test_contexts = [
        {"consciousness_level": 0.9, "emotional_state": "curious"},
        {"consciousness_level": 0.7, "emotional_state": "excited"},
        {"consciousness_level": 0.8, "emotional_state": "empathetic"},
        {"consciousness_level": 0.6, "emotional_state": "contemplative"}
    ]
    
    query = "How does consciousness work?"
    
    for context in test_contexts:
        response = generate_throttled_response(query, context)
        print(f"✅ Level {context['consciousness_level']}, {context['emotional_state']}: {response}")
        
        # Verify consciousness awareness
        assert isinstance(response, str)
        assert len(response) > 40
        # Should reflect the emotional state or consciousness level
        if context["consciousness_level"] > 0.8:
            assert "interesting" in response or "curious" in response or "genuinely" in response
    
    print("🎉 Consciousness-aware formatting tests passed!")

def test_message_naturalization():
    """Test that throttled messages are natural and conversational"""
    print("\n🧪 Testing message naturalization...")
    
    consciousness_context = {
        "consciousness_level": 0.8,
        "emotional_state": "curious"
    }
    
    # Test that base messages are enhanced
    base_messages = [
        "I'm currently processing other requests.",
        "System is busy. Please wait.",
        "Throttled due to high load."
    ]
    
    for base_message in base_messages:
        throttled_result = {
            "response": base_message,
            "status": "throttled"
        }
        
        query = "Hello there!"
        response = extract_response_from_result(throttled_result, query, consciousness_context)
        print(f"✅ Enhanced '{base_message}' → '{response}'")
        
        # Verify enhancement
        assert response != base_message  # Should be enhanced, not just passed through
        assert len(response) > len(base_message)  # Should be more detailed
        assert "Hi" in response or "Hello" in response  # Should be greeting-appropriate
    
    print("🎉 Message naturalization tests passed!")

if __name__ == "__main__":
    print("🚀 Starting throttling integration tests...\n")
    
    try:
        import asyncio
        
        # Run async test
        asyncio.run(test_end_to_end_throttling())
        
        # Run sync tests
        test_different_throttled_scenarios()
        test_consciousness_aware_formatting()
        test_message_naturalization()
        
        print("\n🎉 ALL INTEGRATION TESTS PASSED! 🎉")
        print("✅ Throttled response detection is working correctly")
        print("✅ User-friendly message extraction is functional")
        print("✅ Natural and conversational formatting is active")
        print("✅ Consciousness-aware responses are being generated")
        
    except Exception as e:
        print(f"\n❌ INTEGRATION TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)